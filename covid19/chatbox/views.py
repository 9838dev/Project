from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import user,feed,feed_answer,Trade_feed,raise_issue,feedback

# Create your views here.

#---------------------------------------------------------------------------------------------------------------------------------
#                                              VIEW OF  MAIN UI PAGE
#---------------------------------------------------------------------------------------------------------------------------------
def hello(request):
    if 'Email' in request.session:            #Checking for email present in session or not
        state = user.objects.get(Email = request.session['Email'])
        all_email = user.objects.filter(State=state.State)
        filter_email = []
        for i in all_email:
            filter_email.append(i.Email)
        data=feed.objects.all()                                         # Gathering the data of feed model
        data1=feed_answer.objects.all()                                 # Gathering the data of feed_answer model
        data2=Trade_feed.objects.all()                                  # Gathering the data of Trade_feed model
        data3=user.objects.get(Email=request.session['Email'])          # filtering the data with the help of Email present in user model
        id=request.POST.get('id')                      # Get id from the html page for raise/feed_answer
        delete = request.POST.get('delete')            # Get id from the html page for applying delete operation

        if "feedback" in request.POST:     # If User want to give Feedback
            f = request.POST.get("feedback")
            feedback_data = feedback(Feedback = f,Email=request.session['Email'])
            feedback_data.save()
            return render(request,'index.html',{'key':data,'key1':data1,'key2':data2,'key3':data3.State,'key4':data3.Email,'key5':filter_email})

        if "delete" in request.POST:          # If User want to delete their own query
            del_id = feed.objects.get(id=delete)
            if del_id.Email == request.session['Email']:
                feed_answer.objects.filter(Query_Id=del_id.id).delete()
                feed.objects.filter(id=del_id.id).delete()
            else:
                return HttpResponse("<center><h1>Sorry you cant't delete someone else post.</h1></center>")

        if "raise" in request.POST:          # If User want to raise the issue
            id = request.POST.get('raise')
            if raise_issue.objects.filter(Email=request.session['Email'] , Raise_Id = id):
                print("You already raised")
            else:
                data_raise = raise_issue(Raise_Id = id,Email=request.session['Email'])
                data_raise.save()
                a = feed.objects.get(id = id)
                a.Raise = 1 + int(a.Raise)
                a.save()
                return render(request,'index.html',{'key':data,'key1':data1,'key2':data2,'key3':data3.State,'key4':data3.Email,'key5':filter_email})

        if "action" in request.GET:          # If User want to logout
            action = request.GET.get("action")
            if action == "logout":
                if request.session.has_key('Email'):
                    del request.session['Email']
                return redirect(register)

        if "queries" in request.POST or "answer" in request.POST:   # If User want to raise the queries/feed or answer/feed_answer the queries
            query=request.POST.get('queries')
            answer=request.POST.get('answer')
            if query==None or query=="":
                if answer==None or answer=="":
                    return render(request,'index.html',{'key':data,'key1':data1,'key2':data2,'key3':data3.State,'key4':data3.Email,'key5':filter_email})
                else:
                    answer_data=feed_answer(Query_Id=id,Comment=answer)
                    answer_data.save()
                    return render(request,'index.html',{'key':data,'key1':data1,'key2':data2,'key3':data3.State,'key4':data3.Email,'key5':filter_email})
            else:
                data_save=feed(Query_box=query,Email=request.session['Email'],Raise=1)
                data_save.save()
                return render(request,'index.html',{'key':data,'key1':data1,'key2':data2,'key3':data3.State,'key4':data3.Email,'key5':filter_email})

        if "trade" in request.POST:      # If User want to do business
            trade = request.POST.get('trade')
            if trade==None or trade=="":
                return render(request,'index.html',{'key':data,'key1':data1,'key2':data2,'key3':data3.State,'key4':data3.Email,'key5':filter_email})
            else:
                data_save = Trade_feed(Email=request.session['Email'],Trade=trade)
                data_save.save()
                return render(request,"index.html",{'key':data,'key1':data1,'key2':data2,'key3':data3.State,'key4':data3.Email,'key5':filter_email})

        return render(request,'index.html',{'key':data,'key1':data1,'key2':data2,'key3':data3.State,'key4':data3.Email,'key5':filter_email})

    else:     # If Email is not found in session
        return redirect("register")

#------------------------------------------------------------------------------------------------------------------------------------------
#                                               Login/Signup Page(First page if user is not register)
#------------------------------------------------------------------------------------------------------------------------------------------

def register(request):
    if request.method == "POST" or None:   # If User want to register/Signup
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        state = request.POST.get("state")
        city = request.POST.get('city')
        password = request.POST.get('password')
        rpassword = request.POST.get('rpassword')
        if user.objects.filter(Email=email).exists():    #Checking to existing Email
            return HttpResponse("<center><h1>Email is already exists<br>Please try for another email</h1><center>")

        elif password == rpassword:     # Checking for password and retype password
            data2 = user(Name=name,Email=email,Phone=contact,State=state,City=city,Password=password)
            data2.save()
            request.session['Email'] = email   # Creating a sessions For Email
            return redirect('hello')
        else:
            return HttpResponse("<center><h1>Password Dosent match<h1></center>")

    if request.method == "GET" or None:    # If User want to Login
        if "email" in request.GET and "password" in request.GET:
            email=request.GET.get("email")
            password=request.GET.get("password")
            try:
                data = user.objects.get(Email=email)
                if(data.Password == password):
                    request.session['Email']=email
                    return redirect('hello')
                else:
                    return HttpResponse('<center><h1>wrong password</h1></center>')
            except:
                return render(request,'register.html',{'msg':'Email not found'})


    return render(request,'register.html')

#-------------------------------------------------------------------------------------------------------------------------------------------
#                                                 View for News related Stuff
#-------------------------------------------------------------------------------------------------------------------------------------------

def news(request):
    return render(request,"news.html")

#-------------------------------------------------------------------------------------------------------------------------------------------
#                                                  View for Commonly Asked Question related Stuff
#-------------------------------------------------------------------------------------------------------------------------------------------

def faq(request):
    return render(request,'faq.html')

def terms (request):
    return render (request,'terms.html')
