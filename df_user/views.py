# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from models import *
from hashlib import sha1


def register(request):
    content = {'title': '天天生鲜-注册'}
    return render(request, 'df_user/register.html', content)


def register_exist(request):
    get = request.GET
    uname = get.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({"count": count})


def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    cpwd = post.get('cpwd')
    uemail = post.get('email')
    # 判断用户两次密码输入
    if upwd != cpwd:
        return redirect('/user/register/')
    # 查看用户名是否重复
    if UserInfo.objects.filter(uname=uname):
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd = s1.hexdigest()
    # 创建用户对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd
    user.uemail = uemail
    user.save()
    # 注册成功,转到登录页
    return redirect('/user/login/')


def login(request):
    # 从cookie中得到用户名
    cookie = request.COOKIES
    user_name = cookie.get('user_name', '')
    content = {'title': '天天生鲜-登录', 'error_name': 0, 'error_pwd': 0, 'user_name': user_name}
    return render(request, 'df_user/login.html', content)


def login_handle(request):
    # 处理用户登录
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    # 判断用户名是否存在
    user_list = UserInfo.objects.filter(uname=uname)
    if len(user_list) == 1:
        # 加密密码
        s1 = sha1()
        s1.update(upwd)
        spwd = s1.hexdigest()
        if spwd == user_list[0].upwd:
            hred = HttpResponseRedirect('/user/info/')
            # 登录成功,set-cookie
            if jizhu != 0:
                hred.set_cookie('user_name', uname)
            else:
                # 没有选择记住密码则设置cookie过期
                hred.set_cookie('user_name', '', max_age=-1)
            # 将user_id, user_name存入当前session中(id与name常用)
            request.session['user_id'] = user_list[0].id
            request.session['user_name'] = uname
            return hred
        else:
            # 密码错误
            content = {'title': '天天生鲜-登录', 'error_name': 0, 'error_pwd': 1, 'user_name': uname, 'user_pwd': upwd}
            return render(request, 'df_user/login.html', content)
    else:
        content = {'title': '天天生鲜-登录', 'error_name': 1, 'error_pwd': 0, 'user_name': uname, 'user_pwd': upwd}
        return render(request, 'df_user/login.html', content)


def info(request):

    user = UserInfo.objects.get(pk=request.session['user_id'])
    content = {'title': '天天生鲜-用户中心', 'user_name': user.uname, 'user_email': user.uemail}
    return render(request, 'df_user/user_center_info.html', content)


def order(request):
    content = {'title': '天天生鲜-用户中心'}
    return render(request, 'df_user/user_center_order.html', content)


def site(request):
    addr_list = AddrInfo.objects.filter(user_id=request.session['user_id'])
    # 如果是post请求
    if request.method == 'POST':
        post = request.POST
        if len(addr_list)==0:
            new_addr = AddrInfo()
        else:
            new_addr = addr_list[0]
        new_addr.ushou = post.get('user_shou')
        new_addr.uaddress = post.get('user_addr')
        new_addr.uphone = post.get('user_phone')
        new_addr.uyoubian = post.get('user_youbian')
        new_addr.user = UserInfo.objects.get(pk=request.session['user_id'])
        new_addr.save()

    if len(addr_list)==1:
        content = {'title': '天天生鲜-用户中心', 'addr':addr_list[0]}
    else:
        content = {'title': '天天生鲜-用户中心'}

    return render(request, 'df_user/user_center_site.html', content)
