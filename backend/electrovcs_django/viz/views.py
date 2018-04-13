# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
import shlex
import pam

from glob import glob
from subprocess import Popen, PIPE

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render


@csrf_exempt
def login(request):
    body = json.loads(request.body)
    username = str(body.get('username'))
    password = str(body.get('password'))
    user = authenticate(username, password)
    if not user:
        return HttpResponse(status=401)
    else:
        return HttpResponse()

def authenticate(username, password):
    p = pam.pam()
    if p.authenticate(username, password):
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            user = User(username=username, password='get from PAM')
            user.save()
        return user
    return None

@csrf_exempt
def viz_list(request):
    user = request.user
    # if not user.is_authenticated():
    #     return HttpResponse(status=401)

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

@csrf_exempt
def viz_new(request):
    user = request.user
    #if not user.is_authenticated():
    #     return HttpResponse(status=403)
    if request.method == 'GET':
        return HttpResponse(status=404)

    name = request.POST.get('name')
    user = request.POST.get("user")
    new_viz_dir_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', user, name))
    new_vis_script_path = os.path.join(new_viz_dir_path, name + '.py')
    new_vis_png_path = new_vis_script_path = os.path.join(
        new_viz_dir_path, name)
    if not os.path.exists(new_viz_dir_path):
        os.makedirs(new_viz_dir_path)

    script = json.loads(request.POST.get('script'))
    left = script.split("vcs.init()")
    if len(left) == 1:
        return HttpResponse(status=401)

    canvas_name = left[0].split("=")[0].split('\n')[-1].strip()
    script += "\n{}.png('{}')".format(canvas_name, new_vis_png_path)

    with open(new_vis_script_path+".py", 'w') as fp:
        fp.write(script)
    return HttpResponse()

<<<<<<< HEAD
=======

>>>>>>> 610ff09377f699ad61fd44425d3ba43e9cd5db72
@csrf_exempt
def viz_run(request):
    #user = request.user
    # if not user.is_authenticated():
    #     return HttpResponse(status=401)
    if request.method == 'GET':
        return HttpResponse(status=404)

    name = request.POST.get('name')
    user = request.POST.get("user")
    if not name:
        return HttpResponse(status=401)
    script_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', user, name, name + '.py'))
    if not os.path.exists(script_path):
        return HttpResponse(status=404)

    proc = Popen(shlex.split("python {}".format(script_path)))
    out, err = proc.communicate()
    if err:
        response = json.dumps({'out': out, 'err': err})
        return HttpResponse(response)
