# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect


@login_required(login_url="/login/")
def index(request):
    return redirect('dashboard')  # Redirect to dashboard

@login_required(login_url="/login/")
def dashboard_view(request):
    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(request=request))

@login_required(login_url="/login/")
def pages(request):
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(request=request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(request=request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(request=request))