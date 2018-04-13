# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
import shlex
import pam

from glob import glob
from subprocess import Popen, PIPE
from shutil import copy

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render

# from rest_framework.authtoken.models import Token

def login(request):
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')
    user = authenticate(username, password)
    if not user:
        return HttpResponse(status=401)
    else:
        # token = Token.objects.get(user=user)
        # Response({'token': token.key})
        return HttpResponse()

def authenticate(username, password):
    p = pam.pam()
    if p.authenticate(username, password):
        print 'User: ' + username + ' successfully logged in'
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            # Token.objects.create(user=user)
            user = User(username=username, password='get from PAM')
            user.save()
        return user
    print 'User: ' + username + ' failed to log in'
    return None

@csrf_exempt
def viz_list(request):
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')
    method = body.get('method')
    user = authenticate(username, password)
    if not user:
        print 'No user'
        return HttpResponse(status=401)
    user = str(user)

    # if not user.is_authenticated():
    #     return HttpResponse(status=401)

    user_data_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', user))
    default_data_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'default'))

    if not os.path.exists(user_data_path):
        os.makedirs(user_data_path)

    if method == 'GET':
        script_list = glob(default_data_path)
        script_list += glob(user_data_path)
        response = list()
        for script in script_list:
            contents = os.listdir(script)
            for c in contents:
                response.append(c)
        print 'sending ' + str(response)
        return HttpResponse(json.dumps(response))

    elif method == 'POST':
        new_viz = body.get('name')
        print 'new script ' + new_viz
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
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')
    user = authenticate(username, password)
    if not user:
        return HttpResponse(status=401)

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

@csrf_exempt
def viz_get(request):
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')
    script = body.get('script')
    user = authenticate(username, password)
    if not user:
        return HttpResponse(status=401)
    user = str(user)
    
    user_data_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', user))
    default_data_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'default'))
    
    response = {
        'found': False,
        'img_path': '',
        'script_path': '',
        'contents': ''
    }
    for base_path in [user_data_path, default_data_path]:
        contents = os.listdir(base_path)
        if script in contents:
            response['found'] = True
            script_path = os.path.join(base_path, script, 'script.py')
            if os.path.exists(script_path):
                contents = os.listdir(os.path.join(base_path, script))
                for c in contents:
                    if c.endswith('.png'):
                        response['img_path'] = os.path.join(base_path, script, c)
                        break
                with open(script_path, 'r') as fp:
                    response['script_path'] = script_path
                    for line in fp.readlines():
                        response['contents'] += line
                    
    return HttpResponse(json.dumps(response))

@csrf_exempt
def viz_save(request):
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')
    script = body.get('script')
    script_contents = body.get('contents')

    user = authenticate(username, password)
    if not user:
        print 'No user'
        return HttpResponse(status=401)
    user = str(user)

    user_data_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', user))
    default_data_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'default'))
    
    for base_path in [user_data_path, default_data_path]:
        contents = os.listdir(base_path)
        if script in contents:
            if base_path == default_data_path:
                print 'Attempting to save to default, copying to user data directory'
                script = user + '_' + script
                if not os.path.exists(os.path.join(user_data_path, script)):
                    os.makedirs(os.path.join(user_data_path, script))
                base_path = user_data_path
            script_path = os.path.join(base_path, script, 'script.py')
            with open(script_path, 'w') as fp:
                fp.write(script_contents)
            return HttpResponse()
    return HttpResponse(status=404)

@csrf_exempt
def viz_run(request):
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')
    script = body.get('script')
    user = authenticate(username, password)
    if not user:
        print 'No user'
        return HttpResponse(status=401)
    user = str(user)

    script = script.split('/')[-2]

    user_data_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', user))
    default_data_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'default'))
    script_path = None
    for base_path in [user_data_path, default_data_path]:
        contents = os.listdir(base_path)
        if script in contents:
            if base_path == default_data_path:
                print 'Attempting to run default, copying to user data directory'
                script = user + '_' + script
                if not os.path.exists(os.path.join(user_data_path, script)):
                    os.makedirs(os.path.join(user_data_path, script))
                copy(
                    src=os.path.join(default_data_path, script, 'script.py'),
                    dst=os.path.join(user_data_path, script, 'script.py'))
                base_path = user_data_path
            script_path = os.path.join(base_path, script, 'script.py')
    print 'script_path: ' + script_path
    if not script_path or not os.path.exists(script_path):
        print "cant find script"
        return HttpResponse(status=404)

    cmd = ['python', script_path]
    print 'running ' +  str(cmd)
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    res = {
        'out': out, 
        'err': err,
        'img_path': ''
    }
    head, _ = os.path.split(script_path)
    for c in os.listdir(head):
        if c.endswith('.png'):
            res['img_path'] = os.path.join(head, c)
    print 'returning: ' + str(res)
    return HttpResponse(json.dumps(res))
