from django.shortcuts import render,redirect
from django.http import JsonResponse
from deal.form.login import LoginForm
from .models import FoodTypes,Goods,User,Cart,Order,Message,UserType, Addgoods
import time
import datetime
import random
from django.http import HttpResponse
import os
from django.db import connection
from django.conf import settings
# Create your views here


def mine(request):
    username = request.session.get("username","登录")
    return  render(request,'deal/mine.html',{"title":"我的","username":username})

def login(request):
    if request.method == "POST":
        f = LoginForm(request.POST)
        if f.is_valid():
            # 信息格式没多大问题，验证账号和密码的正确性
            nameid = f.cleaned_data["username"]
            pswd = f.cleaned_data["passwd"]
            print(nameid,pswd)
            try:
                user = User.objects.get(userAccount = nameid)
                if user.userPasswd != pswd:
                    return redirect('/login/')
            except User.DoesNotExist as e:
                return redirect('/login/')

            #登陆成功
            token = time.time() + random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()
            request.session["username"] = user.userName
            request.session["token"] = user.userToken
            return redirect('/mine/')
        else:
            return render(request, 'deal/login.html', {"title": "登陆", "form": f,"error":f.errors})
    else:
        f = LoginForm()
        return render(request, 'deal/login.html', {"title": "登陆","form":f})

def home(request, categoryid, cid, sortid):
    leftSlider = FoodTypes.objects.all()
    print(categoryid, cid, sortid)

    if  cid == '0':
        productList = Goods.objects.filter(categoryid=categoryid)
    elif cid=='1':
        productList = Goods.objects.all()
    else:
        productList = Goods.objects.filter(categoryid=categoryid,childcid = cid)
    # 排序
    if sortid == '1':
        productList = productList.order_by("productnum")
    elif sortid == '2':
        productList = productList.order_by("price")
    elif sortid == '3':
        productList = productList.order_by("-price")

    group = leftSlider.get(typeid = categoryid)
    childList = []
    # "全部分类:0#单反:999#数码相机:998"
    childnames = group.childtypenames
    arr1 = childnames.split("#")
    for str in arr1:
        # 全部分类:0
        arr2 = str.split(":")
        obj = {"childName":arr2[0],"childId":arr2[1]}
        childList.append(obj)

    cartlist = []
    token = request.session.get("token")
    if token:
        user = User.objects.get(userToken = token)
        cartlist = Cart.objects.filter(userAccount = user.userAccount)

    for p in productList:
        for c in cartlist:
            if c.productid == p.productid:
                p.num = c.productnum
                continue

    return render(request, 'deal/home.html',{"title": "主页", "leftSlider": leftSlider,
    "productList": productList, "childList": childList,"categoryid": categoryid, "cid": cid})

#注册
def register(request):
    if request.method == "POST":
        userAccount = request.POST.get("userAccount")
        userPasswd  = request.POST.get("userPass")
        userName    = request.POST.get("userName")
        userPhone   = request.POST.get("userPhone")
        userAdderss = request.POST.get("userAdderss")
        userRank    = 0
        token = time.time() + random.randrange(1, 100000)
        userToken = str(token)
        f = request.FILES["userImg"]
        userImg = os.path.join(settings.MDEIA_ROOT, userAccount + ".png")
        with open(userImg, "wb") as fp:
            for data in f.chunks():
                fp.write(data)
        user = User.createuser(userAccount,userPasswd,userName,userPhone,userAdderss,userImg,userRank,userToken)
        user.save()
        request.session["username"] = userName
        request.session["token"] = userToken
        return redirect('/mine/')
    else:
        return render(request, 'deal/register.html', {"title":"注册"})

def addgoods(request):
    token = request.session.get("token")
    if token == None:
        # 没登录
        return redirect('/login/')
    # (name, longname, productimg, price, marketprice, storenums, specifics, address)
    if request.method == "POST":
        name = request.POST.get("name")
        longname  = request.POST.get("longname")
        productimg=request.FILES["productimg"]
        userImg = os.path.join(settings.IMG_ROOT, name + ".png")
        with open(userImg, "wb") as fp:
            for data in productimg.chunks():
                fp.write(data)
        print(userImg)
        price   = request.POST.get("price")
        marketprice = request.POST.get("marketprice")
        storenum = request.POST.get("storenums")
        specifics = request.POST.get("specifics")
        address = request.POST.get("address")
        storenums=int(storenum)
        print(productimg,address,specifics)
        add = Addgoods.creategoods(name, longname, userImg, price, marketprice, storenums, specifics, address,isDelete=False)
        add.save()
        return redirect('/mine/')
    return render(request, 'deal/addgoods.html')

def cart(request):
    cartslist = []
    token = request.session.get("token")
    if token != None:
        user = User.objects.get(userToken=token)
        cartslist = Cart.objects.filter(userAccount = user.userAccount)
    return render(request, 'deal/cart.html', {"title":"购物车","cartslist":cartslist})

# 修改购物车
def changecart(request,flag):
    # 判断用户是否登录
    token = request.session.get("token")
    if token == None:
        # 没登录
        return JsonResponse({"data":-1, "status":"error"})
    productid = request.POST.get("productid")
    product = Goods.objects.get(productid=productid)
    user = User.objects.get(userToken=token)
    if flag == '0':
        if product.storenums == 0:
            return JsonResponse({"data": -2, "status": "error"})
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        if carts.count() == 0:
            # 直接增加一条订单
            c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg,
                                product.productlongname, False)
            c.save()
            pass
        else:
            try:
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum += 1
                c.productprice = "%.2f" % (float(product.price) * c.productnum)
                c.save()
            except Cart.DoesNotExist as e:
                # 直接增加一条订单
                c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg,
                                    product.productlongname, False)
                c.save()
        # 库存减一
        product.storenums -= 1
        product.save()
        print(c.productprice)
        return JsonResponse({"data": c.productnum, "price": c.productprice, "status": "success"})
    elif flag == '1':
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        if carts.count() == 0:
            return JsonResponse({"data": -2, "status": "error"})
        else:
            try:
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum -= 1
                c.productprice = "%.2f" % (float(product.price) * c.productnum)
                if c.productnum == 0:
                    c.delete()
                else:
                    c.save()
            except Cart.DoesNotExist as e:
                return JsonResponse({"data": -2, "status": "error"})
        # 库存减一
        product.storenums += 1
        product.save()
        print(c.productprice)
        return JsonResponse({"data": c.productnum, "price": c.productprice, "status": "success"})
    elif flag == '2':
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = carts.get(productid=productid)
        c.isChose = not c.isChose
        c.save()
        str = ""
        if c.isChose:
            str = "√"
        return JsonResponse({"data": str, "status": "success"})

def saveorder(request):
    # 判断用户是否登录
    token = request.session.get("token")
    if token == None:
        return JsonResponse({"data":-1, "status":"error"})
    user = User.objects.get(userToken=token)
    carts = Cart.objects.filter(isChose = True)
    if carts.count() == 0:
        return JsonResponse({"data": -1, "status": "error"})

    oid = time.time() + random.randrange(1, 10000)
    oid = "%d"%oid
    o = Order.createorder(oid,user.userAccount,0)
    o.save()
    for item in carts:
        item.isDelete = True
        item.orderid = oid
        item.save()
    return JsonResponse({"status": "success"})

def checkuserid(request):
    userid = request.POST.get("userid")
    try:
        user = User.objects.get(userAccount = userid)
        return JsonResponse({"data":"改用户已经被注册","status":"error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"可以注册","status":"success"})
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/mine/')

def messages(request):
    messages = Message.objects.all()
    return render(request, 'deal/messages.html', {"title": "留言板",'messages': messages})

def create(request):
    return render(request, 'deal/creat.html')

def save(request):
    username = request.POST.get("username")
    title = request.POST.get("title")
    content = request.POST.get("content")
    publish = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = Message.createmessages(username,title,content,publish)
    message.save()
    return redirect('/messages/')

from django.contrib.admin.views.decorators import staff_member_required
def data(request):
    return render(request, 'admin.html')

data = staff_member_required(data)
