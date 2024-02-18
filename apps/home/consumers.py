import ssl
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import os
import redis


class DispositivoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.imei = self.scope['url_route']['kwargs']['imei']
        await self.accept()

        # Configuración de Redis
        self.r = redis.Redis(
            host=os.getenv('REDIS_HOST', 'us1-climbing-cowbird-40081.upstash.io'),
            port=int(os.getenv('REDIS_PORT', 40081)),
            password=os.getenv('REDIS_PASSWORD', '1212460ce61a4ef6b549248b4fd9d9a0'),
            ssl=True,
            ssl_cert_reqs=ssl.CERT_NONE  # Desactivar la verificación del certificado SSL
        )

        self.pubsub = self.r.pubsub()
        self.pubsub.subscribe('ubicaciones', 'codec12_responses')

        # Iniciar la tarea de escuchar mensajes de Redis
        asyncio.get_event_loop().create_task(self.listen_to_redis())

    async def disconnect(self, close_code):
        self.pubsub.unsubscribe('ubicaciones', 'codec12_responses')
        self.pubsub.close()

    async def receive(self, text_data):
        # Aquí puedes manejar los datos recibidos del WebSocket
        pass

    async def listen_to_redis(self):
        while True:
            message = await self.loop.run_in_executor(None, self.pubsub.get_message)
            if message and message['type'] == 'message':
                if message['channel'].decode('utf-8') == 'ubicaciones':
                    location_data_str = message['data'].decode('utf-8')
                    location_data = json.loads(location_data_str)
                    await self.send(text_data=json.dumps({'type': 'location', 'data': location_data}))
                elif message['channel'].decode('utf-8') == 'codec12_responses':
                    codec12_data_str = message['data'].decode('utf-8')
                    codec12_data = json.loads(codec12_data_str)
                    await self.send(text_data=json.dumps({'type': 'codec12', 'data': codec12_data}))
            await asyncio.sleep(1)  # Para evitar sobrecargar el loop
