from django.shortcuts import render, render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from onlinecompiler import models

import os.path, os, subprocess

# save cu file
def save_cu_file(code):
    file_name = "example.cu"
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    file_path = os.path.join(path, 'cudafiles', file_name)
    with open(file_path, 'w+') as f:
        code = '''{0}'''.format(code)
        f.write(code)
    return file_path

def compile_and_executte(path):
    name = os.path.split(path)[1] # return file name
    name = os.path.splitext(name)[0] # enclude file extension
    command = r"nvcc {0} -o {1}".format(path, name)
    return_code = None
    try:
        return_code = subprocess.call(command) # if nvcc compiles successfully, return 0
    except Exception as e:
        return e
    if (return_code == 0):
        execute_file = os.path.join(name, '.exe')
        result = os.system(execute_file)
           
        
# Create your views here.
@csrf_exempt
def compile(request):
    if request.method == 'POST':
        code = request.POST['code']
        models.Compile.objects.create(name=code) # save code to database
        save_cu_file(code)
        
        file_path = save_cu_file(code)
        compile_and_executte(file_path)
        
    return render_to_response("index.html", {})