from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth

from .models import destination
def req(request):
    context={}
    context['form']=fdata()
    #request.POST.get['first_name']
    return render(request,"hel.html",context)
    
def ren(request):
    namme=request.POST['first_name']
    return render(request,"result.html",{'result':namme})

def view(request):
    dest1=destination()
    dest1.name="suraj city"
    dest1.desc="kill anyone"

    
    return render(request,"index.html",{'dest1':dest1})

def log(request):
    if request.method == 'POST':

        first_name=request.POST['first_name']
        second_name=request.POST['second_name']
        user=request.POST['user']
        pswd=request.POST['pass']

        u=User.objects.create_user(username=user,password=pswd,first_name=first_name,last_name=second_name)
        u.save();
        return redirect('/')
        
    else:
        return render(request,'login.html')



    






# Create your views here.
