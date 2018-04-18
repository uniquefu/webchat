from django.shortcuts import render,HttpResponse,redirect
from app01.form import form
from io import BytesIO
from utils.check_code import create_validate_code
from . import models
from utils.auth import check_login
import json,time,queue

GLOBAL_QUEUE ={}
# Create your views here.
def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

def register(request):
    if request.method =="GET":
        obj =form.Register(request=request)
        return render(request,'register.html',{'obj':obj})

    elif request.method =='POST':
        obj =form.Register(request=request,data=request.POST)

        if obj.is_valid():
            print(obj.cleaned_data)
            del obj.cleaned_data['repassword']
            del obj.cleaned_data['check_code']

            models.UserInfo.objects.create(**obj.cleaned_data)
            return redirect('/webchat.html')
        else:
            print(obj.errors)
            return render(request, 'register.html', {'obj': obj})

def logout(request):
    request.session.clear()

    return redirect('/')

def login(request):
    if request.method =="GET":
        obj =form.LoginForm(request=request)
        return  render(request,'login.html',{"obj":obj})

    elif request.method =="POST":
        result = {'status': False, 'message': None, 'data': None}
        obj = form.LoginForm(request=request, data=request.POST)

        if obj.is_valid():
            print(obj.cleaned_data)
            u=obj.cleaned_data['username']
            p=obj.cleaned_data['password']
            user_info=models.UserInfo.objects.filter(username=u,password=p).\
                values('nid','username','nickname','email','brief',\
                       'avatar').first()

            if not user_info:
                result['message']="用户名或密码错误"
            else:
                result['status']=True
                request.session['user_info']=user_info

                if obj.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 31)
        else:
            print(obj.errors)
            if 'check_code' in obj.errors:
                result['message'] = '验证码错误或者过期'
            else:
                result['message'] = '用户名或密码错误'
        print(result)
        return HttpResponse(json.dumps(result))



@check_login
def webchat(request):
    status_id =models.UserInfo.status_choices
    nid = request.session['user_info']['nid']
    obj =models.UserInfo.objects.filter(nid=nid).first()
    request.session['user_info']['status_id']=status_id
    return render(request,'chat.html',{'obj':obj})

@check_login
def msg_send(request):
    #if request.method =="POST":
        data = request.POST.get('data')

        if data:
            msg_data= json.loads(data)
            msg_data['timestamp']=time.time()
            if msg_data["con_type"] =="single":
                if not GLOBAL_QUEUE.get(int(msg_data['to'])):
                    GLOBAL_QUEUE[int(msg_data['to'])] = queue.Queue()
                GLOBAL_QUEUE[int(msg_data['to'])].put(msg_data)
        return  HttpResponse("-----MSG received----------")

@check_login
def get_msg(request):
    nid = request.session['user_info']['nid']
    if not nid in GLOBAL_QUEUE:
        GLOBAL_QUEUE[nid] = queue.Queue()
    msg_count = GLOBAL_QUEUE[nid].qsize()
    msg_list=[]
    if msg_count>0:
        for item in range(msg_count):
            print(GLOBAL_QUEUE[nid])
            msg_list.append(GLOBAL_QUEUE[nid].get())
    else:
        try:
            msg_list.append(GLOBAL_QUEUE[nid].get(timeout=60))

        except queue.Empty:
            print("接收时间超时")
    return HttpResponse(json.dumps(msg_list))