from django.shortcuts import render,redirect
from.models import Profile,Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm,ProfileForm,SkillForm,MessageForm
from .utils import searchProfiles,paginateProfiles
from django.contrib.auth.decorators import login_required


# Create your views here.
def profiles(request):
    
    #profiles = Profile.objects.all()
    profiles,search_query= searchProfiles(request)
    profiles,custom_range = paginateProfiles(request,profiles,3)
    context = {
        'profiles':profiles,
        'search_query':search_query,
        'custom_range':custom_range,
        
    }
    return render(request,'users/profiles.html',context)


def profile(request,pk):
    profile = Profile.objects.get(id=pk)
    topskills = profile.skill_set.exclude(description="")
    otherskills = profile.skill_set.filter(description="")
    context ={
        'profile':profile,
        'topskills':topskills,
        'otherskills':otherskills,
        }
    return render(request,'users/single-profile.html',context)

def loginUser(request):
    
    if request.method == 'POST':
    
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User is not available')
            
            
        user = authenticate(request,username=username,password=password)
            
        if user is not None:
            
            login(request,user)
                
            return redirect(request.GET['next'] if 'next' in request.GET else 'Users:account')
        else:
            
            messages.error(request,'username and password doesnt match')
                
            
    return render(request,'users/login-register.html')

def logoutUser(request):
    logout(request)
    messages.info(request,'User successfully loggedout')
    return redirect('Users:login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'User succesfully created')
            return redirect('Users:login')
        else:
            messages.error(request,'Some error occured')
        
    context = {
        'page':page,
        'form':form,
    }
    return render(request,'users/login-register.html',context)


def userAccount(request):
    profile = request.user.profile
    context ={
        'profile':profile,
    }
    
    return render(request,'users/account.html',context)


def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid:
            form.save()
            messages.success(request,'profile updated')
            return redirect('Users:account')
        else:
            messages.error(request,'Enter valid data in fields')
            
    context = {
        'form':form,
    }  
    return render(request,'users/profile-form.html',context)  



def createSkill(request):
    profile = request.user.profile
    form = SkillForm() 
    if request.method == 'POST':
        form = SkillForm(request.POST) 
        if form.is_valid():
           skill =  form.save(commit=False) 
           skill.owner = profile
           skill.save()
           messages.success(request,'skill created successfully')
           return redirect('Users:account')
        else:
            messages.error(request,'some error occured')
        
    context = {
        'form':form,
        }
    return render(request,'users/skill-form.html',context)



def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)
        
        if form.is_valid():
            form.save()
            messages.success(request,'skill updated successfully')
            
            return redirect('Users:account')
        else:
            messages.error(request,'some error occured')
            
    context = {
        'form':form
    }        
    
    return render(request,'users/skill-form.html',context)




def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    
    if request.method =="POST":
        skill.delete()
        messages.success(request,'skill deleted successfully')
        
        return redirect('Users:account')
    
    context ={
        'object':skill,
    }
    return render(request,'projs/delete-project.html',context)


@login_required(login_url='Users:login')
def inbox(request):
    recipient = request.user.profile
    recieved_msgs = recipient.messages.all()
    unreadCount = recieved_msgs.filter(is_read=False).count()
    
    context = {
        'recieved_msgs':recieved_msgs,
        'unreadCount':unreadCount,
    }
    return render(request,'users/inbox.html',context)


@login_required(login_url='Users:login')
def viewMessage(request,pk):
    message = Message.objects.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    
    context = {
        'message':message,
    }    
    return render(request,'users/message.html',context)


def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        
        try:
            sender = request.user.profile
        except:
            sender = None
            
        if form.is_valid():
            message = form.save(commit=False) 
            message.sender = sender
            message.recipient = recipient 
                
            if sender:
                message.name = sender.name 
                message.email = sender.email
            message.save()
            print('message saved')
                    
            return redirect('Users:profiles-all')     
        
    context = {
        'recipient':recipient,
        'form':form,
    }
    return render(request,'users/message-form.html',context)


def deleteAccount(request):
    profile = request.user.profile
    
    
    if request.method == 'POST':
        profile.delete()
        
        messages.success(request,'profile deleted successfully')
        return redirect('Users:profiles-all')
    
            
    context = {
        'object':profile,
    }  
    return render(request,'projs/delete-project.html',context) 
    
    
    
    
