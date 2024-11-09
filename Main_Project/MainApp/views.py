from django.shortcuts import render,redirect
from.models import productdata,cart,order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q
import random
import razorpay
# Create your views here.

def home(request):
    return render(request,'home.html')


def navbar(request):
    return render (request,'navbar.html')


def footer(request):
    return render (request,'footer.html')

def product(request):
    context={}
    p=productdata.objects.filter(is_active=True)
    context['products']=p
    return render (request,'product.html',context)

def pdetails(request,pid):
    p=productdata.objects.filter(id=pid)
    context={}
    context['products']=p
    return render (request,'productDetails.html',context)


def productpagi(request):
    plist=productdata.objects.all()
    page=request.GET.get('page',1)

    paginator=Paginator(plist,5)
    try:
        products=paginator.page(page)
    except PageNotAnInteger:
        products=paginator.page(1)
    except EmptyPage:
        products=paginator.page(paginator.num_pages)   

    return render(request,'product.html',{'products':products}) 


def sort(request,sv):
    if sv == '0':
        col='price' 

    else:
        col ='-price'  
    p=productdata.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'product.html',context)   

def range(request):
    if request.method =='POST':
       min=request.POST.get('min')
       max=request.POST.get('max')
       q1=Q(price__gte=min)
       q2=Q(price__lte=max)
       q3=Q(is_active=True)
       p=productdata.objects.filter(q1 & q2 & q3)
       context={}
       context['products']=p
       return render(request,'product.html',context)



def pcatfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(pcat=cv)
    p=productdata.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'product.html',context)



def user_login(request):        
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=="" or upass=="":
            context={}
            context['errormsg']="Field can't be empty- plz check it out !"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)   
            if u is not None:
                login(request,u)
                return redirect('/')
            else:
                context={}
                context['errormsg']="Invalid username and password "
                return render(request,'login.html',context)  
                   
    else:
        return render(request,'login.html')



def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        uemail=request.POST['uemail']
        ucpass=request.POST['ucpass']   
        if uname=="" or upass=="" or ucpass=="":  
            context={}
            context['errormsg']="Field can't be empty- plz check it out !"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context={}
            context['errormsg']="Password didn't match- plz check it out !"
            return render(request,'register.html',context)
        else:

            try:
                u=User.objects.create(username=uname,password=upass,email=uemail)
                u.set_password(upass) 
                u.save()
                context={}
                context['success']="User created successfully"
                return render(request,'register.html',context)
        
            except Exception:
                context={}
                context['errormsg']="Username already exist"
                return render(request,'register.html',context)   
                  
    else:
        return render(request,'register.html')
    
    
def user_logout(request):
    logout(request)
    return redirect('/')


def contact(request):
    return render (request,'contact.html')

def about(request):
    return render (request,'about.html')    


def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u[0])
        p=productdata.objects.filter(id=pid)
        print(p[0])
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=cart.objects.filter(q1 and q2)
        n=len(c)
        print(n)
        context={}
        context['products']=p
        if n == 1:
            context['success']="Product already exist"
        else:
            c=cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="procust added successfully in cart "

        return render(request,'productDetails.html',context)
    
    else:
        return redirect('/login')   



def viewcart(request):
    if request.user.is_authenticated:
        c=cart.objects.filter(uid=request.user.id)
        np=len(c)
        s=0
        for x in c:
           s=s+x.pid.price*x.qty
        print(s)    
        context={}
        context['products']=c
        context['total']=s
        context['n']=np
        return render(request,'cart.html',context)
    
    else:
        return redirect('/login')
    


def updateqty(request,qv,cid):
    c=cart.objects.filter(id=cid) 
    if qv =='1': 
        t=c[0].qty+1
        c.update(qty=t)

    else:
        if c[0].qty > 1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/viewcart')


def remove(request,cid):
    c=cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')


def placeorder(request):
    userid=request.user.id
    c=cart.objects.filter(uid=userid)
    oid=random.randrange(100,9999)
    for x in c:
        o=order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete() # delete record from cart table 
    orders=order.objects.filter(uid=request.user.id)
    context={}
    context['products']=orders
    np=len(orders)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
    context['total']=s
    context['n']=np

    return render(request,'placeorder.html',context)    


def makepayment(request):
    orders=order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty*100
        oid=x.order_id
        
    print(oid)
    client = razorpay.Client(auth=("rzp_test_t3q4uoB0Hc14De", "6dqrlj1EtBqOjDoEjRjSe60w"))
    data = { "amount": s, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    return render(request,"home.html",context)
    
