# -*- coding: utf-8 -*-
import os
import json
import shlex
from glob import glob
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from subprocess import Popen, PIPE


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


def viz_new(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(status=401)
    if request.method == 'GET':
        return HttpResponse(status=404)

    name = request.POST.get('name')
    new_viz_dir_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', user, name))
    new_vis_script_path = os.path.join(new_viz_dir_path, name + '.py')
    new_vis_png_path = new_vis_script_path = os.path.join(
        new_viz_dir_path, name + '.png')
    if not os.path.exists(new_viz_dir_path):
        os.makedirs(new_viz_dir_path)

    script = json.loads(request.POST.get('script'))
    left = script.split("vcs.init()")
    if len(left) == 1:
        return HttpResponse(status=401)

    canvas_name = left[0].split("=")[0].split('\n')[-1].strip()
    script += "\n{}.png({}".format(canvas_name, new_vis_png_path)

    with open(new_vis_script_path, 'r') as fp:
        fp.write(script)
    return HttpResponse()


def viz_run(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(status=401)
    if request.method == 'GET':
        return HttpResponse(status=404)

    name = request.POST.get('name')
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
