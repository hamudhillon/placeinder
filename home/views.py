from bs4 import BeautifulSoup
import json
import xlwt
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
import re
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from home.models import Imagelist
from home.models import UserImagelist
import uuid
from django.shortcuts import redirect


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def index(request):
    response = {
        'message': 'Welcome to SourceValidation API'
    }
    return Response(response)


@login_required(login_url='/login/')
def tinder(request):

    global main
    # lst = Imagelist.objects.all()
    return redirect(login1)


global res
res = []

global rdict


def ulist(request, uname):
    print(uname)
    lst = UserImagelist.objects.filter(
        uuid=uname).values('name', 'url').distinct()
    print(lst)
    return render(request, 'userlist.html', {'ulist': lst})


def form(request):
    return render(request, 'list.html')


def form_res(url):
    import requests
    from bs4 import BeautifulSoup

    con = requests.get(url)
    soup = BeautifulSoup(con.content, u'html.parser')
    # print(soup.find('div',attrs={'class':'resultsTable'}))
    return soup.find('div', attrs={'class': 'resultsTable'})


def result(request):
    import json
    poo = request.GET
    pool = poo.values()
    str1 = ""
    for r in pool:
        str1 += r+', '
    link = 'https://mylongevity.com.au/Analyser.aspx?PageSection=PageResult&Pool='+str1
    url = link.replace('",', ',')
    print(url)
    div = form_res(url)
    return HttpResponse(div)


def like(request):
    uid = request.user.id

    # return render(request, 'index.html', {'images': lst})
    try:
        import simplejson as json
    except:
        import json
    url = request.GET.get('url')
    uname = request.GET.get('name')
    load = request.GET.get('load')
    uuser = request.GET.get('user')
    print(uname)
    if load == 'reload':
        print("reloading.......")
        res.clear()
        # main.remove()
    urls = str(url).replace('"', '').strip()
    ll = str(urls) + '|name ' + str(uname)
    save_file = request.GET.get('save')
    # print(url)

    dicts = {"url": url, "name": uname}
    # print('TEST ->>', dicts)

    res.append(ll)
    main = list(dict.fromkeys(res))
    # print(res[-1]['url'])
    # if res[-1]['url']!=dicts['url']:
    #     main.append(dicts)
    try:
        ress = json.dumps(main)
    except:
        import sys
        # print(sys.exc_info())
    # print(ress)
    # print(type(ress))
    if uname != None:
        list_c = UserImagelist.objects.filter(
            user_id=uid, url=url, name=uname, uuid=uuser).count()
        print("Count ->"+str(list_c))
        if list_c == 0:
            ulst = UserImagelist()
            ulst.name = uname
            ulst.url = url
            ulst.User = uuser
            ulst.user_id = uid
            ulst.uuid = uuser
            ulst.save()

    if save_file == 'save':
        lst = UserImagelist.objects.filter(
            user_id=uid).values('name', 'url').distinct()
        Ilist = []
        for l in lst:
            Ilist.append(l)

        print(Ilist)

        ress = json.dumps(Ilist)
    return HttpResponse(ress)


def home(request):

    import requests

    r = 0
    for i in range(1, 2):
        try:
            con = requests.get(
                url='https://www.listchallenges.com/bucket-list-500-fascinating-cities-of-the/list/'+str(i))
            soup = BeautifulSoup(con.content, u'html.parser')
            listt = soup.findAll('div', attrs={'class': 'list-item'})
        except:
            continue
        for l in listt:
            try:
                name = l.find('div', attrs={'class': 'item-name'}).text.strip()
            except:
                name = ''
            try:
                img_url = l.find('img')['src']
                if 'loading.png' in img_url:
                    img_url = l.find('img')['data-src']
                img_url = 'https://www.listchallenges.com'+str(img_url)
            except:
                img_url = ''
            r += 1
            lst = Imagelist()
            lst.name = name
            lst.url = img_url
            print(name, img_url)
            lst.save()
    return render(request, 'homepage.html')


@login_required(login_url='/login/')
def roompage(request):
    return render(request, 'room.html')


def craeteusername(email):
    username = email.split("@")[0]
    username = re.sub('[^A-Za-z0-9\.]+', '', username)
    username = username.lower()
    orignam_uname = username
    exists = True
    count = 1
    while exists:
        exists = User.objects.filter(username=username).exists()
        if exists:
            if count < 10:
                username = orignam_uname + "0" + str(count)

            else:
                username = orignam_uname + str(count)
            count += 1
    return username.lower()


def Token_register(request):
    try:
        lastname = ''
        token_key = None
        msg = None
        if request.method == "POST":
            exists_check = request.POST.get('txt_email')

            user_msg = User.objects.filter(email=exists_check).count()
            if user_msg > 0:
                msg = 'Email Already Exists'
            else:
                usr_password = request.POST.get('txt_password')
                objU = User()
                objU.first_name = request.POST.get('txt_fname')
                objU.last_name = lastname
                username = craeteusername(request.POST.get(
                    'txt_email'))  # create username from email
                objU.username = username
                objU.email = request.POST.get('txt_email')
                objU.password = usr_password
                objU.set_password(objU.password)
                objU.is_active = True
                objU.is_superuser = False
                objU.is_staff = False
                objU.save()
                token = Token.objects.create(user=objU)
                token_key = token.key
        return render(request, 'Token_register.html', {"token": token_key, "msg": msg})

    except:
        import sys
        return HttpResponse(str(sys.exc_info()))


def login1(request):
    msg = None
    if request.method == "POST":
        username = request.POST.get('txt_username')
        password = request.POST.get('txt_password')
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):

                objuser = user
            else:
                objuser = None

        except:
            objuser = None

        if objuser is not None:
            if objuser.is_active:
                login(request, objuser)
                token = Token.objects.get_or_create(user=objuser)
                token = token[0]
                token_key = token.key
                msg = token_key
                lst = Imagelist.objects.all()
            return render(request, 'index.html', {"msg1": msg, "user": user, 'images': lst})
            # return HttpResponseRedirect('/room/')
        else:
            msg = 'Wrong Password'
    return render(request, 'login.html', {"msg1": msg})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')
