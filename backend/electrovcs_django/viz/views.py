# -*- coding: utf-8 -*-
import os
import json
from glob import glob
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render


def viz_list(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(status=401)

    user_data_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', user))
    default_data_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'default'))

    if not os.path.exists(user_data_path):
        os.makedirs(user_data_path)

    if request.method == 'GET':
        response = glob(default_data_path)
        response += glob(user_data_path)
        response = json.dumps(response)
        return HttpResponse(response)

    elif request.method == 'POST':
        new_viz = request.POST.get('name')
        if not new_viz:
            return HttpResponse(status=400)
        new_data_path = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', 'data', user, new_viz))
        if os.path.exists(new_data_path):
            return HttpResponse(status=400)
        os.makedirs(new_data_path)
        return HttpResponse()
    else:
        return HttpResponse(status=404)
