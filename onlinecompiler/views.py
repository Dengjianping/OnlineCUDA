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
    with open(file_path, 'w+', newline="\n") as f:
        code = '''{0}'''.format(code)
        f.write(code)
    return file_path

# compile cuda source file and execute it
def compile_and_executte(path):
    name = os.path.split(path)[1] # return file name
    name = os.path.splitext(name)[0] # enclude file extension
    output_path = os.path.join('onlinecompiler', 'cudafiles', name)
    command = r"nvcc {0} -o {1}".format(path, output_path)
    return_code = None
    compile_status = None
    try:
        compile_status = subprocess.Popen(command, stdout=subprocess.PIPE) # if nvcc compiles successfully, return 0
        compile_result = compile_status.communicate()
        return_code = compile_status.wait(60)
    except Exception as e:
        print("sds")
        return compile_status, return_code
    if (return_code == 0):
        execute_file = name + '.exe'
        path = os.path.dirname(path)
        execute_file = os.path.join(path, execute_file)
        result = subprocess.Popen(execute_file, stdout=subprocess.PIPE)
        stdout = result.communicate()
        exit_code = result.wait(60)
        return stdout, exit_code
        
# Create your views here.
@csrf_exempt
def compile(request):
    code = ''
    result = None
    if request.method == 'POST':
        code = request.POST['q']
        # models.Compile.objects.create(name=code) # save code to database
        file_path = save_cu_file(code)
        execute_code = None
        try:
            result, execute_code = compile_and_executte(file_path)
            result = result[0]
        except:
            pass
        if (execute_code != 0):
            print(result)
        
    return render_to_response("index.html", {'code': code, 'result': result})