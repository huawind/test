from django.db import models

# Create your models here.


# 用户模型类
class User(models.Model):

    # 用户账号，要唯一
    userAccount = models.CharField(max_length=20,verbose_name='学号',unique=True)
    # 密码
    userPasswd  = models.CharField(max_length=20,verbose_name='密码')
    # 昵称
    userName    =  models.CharField(max_length=20,verbose_name='昵称')
    # 手机号
    userPhone   = models.CharField(max_length=20,verbose_name='手机号')
    # 地址
    userAdderss = models.CharField(max_length=100,verbose_name='地址')
    # 头像路径
    userImg     = models.CharField(max_length=150,verbose_name='头像')
    # 等级
    userRank    = models.IntegerField(verbose_name='等级')
    # touken验证值，每次登陆之后都会更新
    userToken   = models.CharField(max_length=50)

    def __str__(self):
        return self.userName

    @classmethod
    def createuser(cls,account,passwd,name,phone,address,img,rank,token):
        u = cls(userAccount = account,userPasswd = passwd,userName=name,userPhone=phone,userAdderss=address,userImg=img,userRank=rank,userToken=token)
        return u


# 分类模型
class FoodTypes(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=20)
    typesort = models.IntegerField()
    childtypenames = models.CharField(max_length=150)
    def __str__(self):
        return self.typename

# 商品模型类
class Goods(models.Model):
    # 商品id
    productid = models.CharField(max_length=10,verbose_name='商品id')
    # 商品图片
    productimg = models.CharField(max_length=150,verbose_name='商品图片')
    # 商品名称
    productname = models.CharField(max_length=50,verbose_name='商品名称')
    # 商品长名称
    productlongname = models.CharField(max_length=100,verbose_name='商品长名称')
    # 是否精选
    isxf = models.NullBooleanField(default=False,verbose_name='是否精选')
    # 是否买一赠一
    pmdesc = models.CharField(max_length=10,verbose_name='是否买一赠一')
    # 规格
    specifics = models.CharField(max_length=20,verbose_name='规格')
    # 价格
    price = models.CharField(max_length=10,verbose_name='价格')
    # 原价价格
    marketprice = models.CharField(max_length=10,verbose_name='原价价格')
    # 组id
    categoryid = models.CharField(max_length=10,verbose_name='组id')
    # 子类组id
    childcid = models.CharField(max_length=10,verbose_name='子类组id')
    # 子类组名称
    childcidname = models.CharField(max_length=10,verbose_name='子类组名称')
    # 详情页id
    dealerid = models.CharField(max_length=10,verbose_name='详情页id')
    # 库存
    storenums = models.IntegerField(verbose_name='库存')
    # 销量
    productnum = models.IntegerField(verbose_name='销量')

    def __str__(self):
        return self.productname


class CartManager1(models.Manager):

    def get_queryset(self):
        return super(CartManager1, self).get_queryset().filter(isDelete=False)
class CartManager2(models.Manager):

    def get_queryset(self):
        return super(CartManager2, self).get_queryset().filter(isDelete=True)


class Cart(models.Model):
    userAccount = models.CharField(max_length=20)
    productid = models.CharField(max_length=10)
    productnum = models.IntegerField()
    productprice = models.CharField(max_length=10)
    isChose = models.BooleanField(default=True)
    productimg = models.CharField(max_length=150)
    productname = models.CharField(max_length=100)
    orderid = models.CharField(max_length=20,default="0")
    isDelete = models.BooleanField(default=False)
    objects = CartManager1()
    obj2 = CartManager2()

    @classmethod
    def createcart(cls,userAccount,productid,productnum,productprice,isChose,productimg,productname,isDelete):
        c = cls(userAccount = userAccount,productid = productid,productnum=productnum,productprice=productprice,isChose=isChose,productimg=productimg,productname=productname,isDelete=isDelete)
        return c


class Order(models.Model):
    orderid = models.CharField(max_length=20)
    userid  = models.CharField(max_length=20)
    progress = models.IntegerField()

    @classmethod
    def createorder(cls, orderid, userid, progress):
        o = cls(orderid=orderid, userid=userid, progress=progress)
        return o


class UserType(models.Model):
    name = models.CharField(max_length=32,verbose_name='用户类型')

    def __str__(self):
        return self.name


class Message(models.Model):
    username = models.CharField(max_length=256)
    title = models.CharField(max_length=512)
    content = models.TextField(max_length=256)
    publish = models.DateTimeField()

    # 为了显示
    @classmethod
    def createmessages(cls, username, title, content, publish):
        messages = cls(username=username, title=title, content=content, publish=publish)
        return messages


class Addgoods(models.Model):
    name = models.CharField(max_length=20)
    longname = models.CharField(max_length=150)
    productimg = models.CharField(max_length=150)
    # 价格
    price = models.CharField(max_length=10,verbose_name='价格')
    # 原价价格
    marketprice = models.CharField(max_length=10,verbose_name='原价价格')
    # 库存
    storenums = models.IntegerField(verbose_name='库存')
    specifics = models.CharField(max_length=20,verbose_name='规格')
    address = models.CharField(max_length=10,verbose_name='地址')
    isDelete = models.BooleanField(default=False)

    @classmethod
    def creategoods(cls,name,longname,productimg,price,marketprice,storenums,specifics,address,isDelete):
        c = cls(name = name,longname = longname,productimg=productimg,price=price,marketprice=marketprice,storenums=storenums,
                specifics=specifics,address=address,isDelete=isDelete)
        return c