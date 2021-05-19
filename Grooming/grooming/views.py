from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .models import users_data , shops_data ,shop_service

def home (request):
    if request.method =="GET":
        if "Email" in request.session:
            Email = request.session["Email"]
            temp_data = users_data.objects.get(Email=Email )
            temp_locality = temp_data.Locality
            data = shops_data.objects.filter(Locality=temp_locality)
            if 'action' in request.GET:
                action = request.GET.get('action')
                if action == 'logout':
                    if request.session.has_key('Email'):
                        request.session.flush()
                        return redirect('user_login')
            if 'box' in request.GET :
                search = request.GET.get('box')
                search_data = shops_data.objects.filter(Shopname=search)
                return render (request,'user_ui.html',{"key":search_data})
            return render (request,'user_ui.html',{"key":data,})
        else:
            return redirect ('user_login')

def user_login (request):
    if request.method == "POST"  :
        Email = request.POST["Email"]
        Password = request.POST["Password"]
        try:
            temp_data = users_data.objects.get(Email=Email )
            temp_pass = (temp_data.Password)
            if temp_pass == Password :
                request.session['Email'] = Email
                return redirect ('home')
            else:
                return render (request,'user_login.html', {"msg3":"You have enterd wrong credentials"})
        except :
            return render (request,'user_login.html',{"msg1":"Email does not exist"})
    return render (request,'user_login.html',)

def user_reg(request):
    if request.method == "POST" :
        Name = request.POST["Name"]
        Gender = request.POST ["Gender"]
        Email = request.POST["Email"]
        Contact = request.POST["Contact"]
        Password = request.POST["Password"]
        Re_password = request.POST["Re-password"]
        Locality = request.POST["Locality"]
        info = {"key":"Your password dosent match "}
        if Password == Re_password :
            data = users_data(Name=Name,Gender=Gender,Email=Email,Contact=Contact,Password=Password,Locality=Locality)
            data.save()
            return redirect('user_login')
        else:
            return render(request,'user_reg.html',{"msg2":"Your password doesnot match"})

    return render(request,'user_reg.html')

def shop_reg (request):
    if request.method == "POST":
        Name      =request.POST["Name"]
        Gender    =request.POST["Gender"]
        Shopname  =request.POST["Shopname"]
        Service   = request.POST["Services"]
        Email     = request.POST["Email"]
        Contact   = request.POST["Contact"]
        Password  = request.POST["Password"]
        Re_password =request.POST["Re-password"]
        Locality    =request.POST["Locality"]
        if Password == Re_password:
            data = shops_data(Name=Name,Gender=Gender,Shopname=Shopname,Service=Service,Email=Email,Contact=Contact,Password=Password,Locality=Locality,)
            data.save()
            return redirect ('shop_login')
        else:
            return render (request,'shopkeeper_reg.html',{"key":"Your password dosent match"})
    return render (request,'shopkeeper_reg.html')

def shop_login(request):
    if request.method == "POST":
        Email = request.POST["Email"]
        Password = request.POST["Password"]
        try:
            temp_data = shops_data.objects.get(Email=Email)
            temp_pass = temp_data.Password
            if (temp_pass == Password):
                request.session['shop']=Email
                return redirect ('shop_ui')
            else:
                return render (request,"shopkeeper_login.html",{"key1":"You have enterd wrong credentials"})
        except:
            return render (request,"shopkeeper_login.html",{"key":"Email does not exist"})

    return render (request,'shopkeeper_login.html')

def shop_ui (request):
    if request.method =="GET":
        if "shop" in request.session:
            temp_email=request.session['shop']
            temp_data = shop_service.objects.filter(Email=temp_email)
            return render(request,'shop_ui.html',{"key":temp_data})
        else:
            return redirect ('shop_login')

def shop_logout(request):
    request.session.flush()
    return redirect('shop_login')

def shop_services (request):
    temp_email=request.session['shop']
    temp_data = shop_service.objects.filter(Email=temp_email)
    service=request.GET.get('service')
    price=request.GET.get('price')
    temp_id=request.GET.get('id')
    if 'del' in request.GET:
        del_data = shop_service.objects.filter(id=temp_id)
        del_data.delete()
        return redirect("shop_services")
    if 'save' in request.GET :
        if service == "":
            return render(request,"shop_services.html",{"msg":"Please Enter something"})
        if service != None:
            data = shop_service(Email=temp_email,Service=service,Price=price)
            data.save()
            return redirect("shop_services")
    return render(request,"shop_services.html",{"key":temp_data})

def user_service_interface(request):
    temp_email=request.GET.get("ref")
    data = shops_data.objects.get(Email=temp_email)
    service_data=shop_service.objects.filter(Email=temp_email)
    return render(request,'user_service_interface.html',{"key":data,"key1":service_data})

def test(request):
    print(request.method)
    print(request.GET)
    print(request.GET.get('service'))
    print(request.GET.get('lol'))
    if 'lol' in request.GET:
        print("lol")
    if 'service' in request.GET:
        print("lol")
    if request.method=="POST":
        print(request.POST['data'])

    return render(request,'test.html')
