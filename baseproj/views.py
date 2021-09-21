from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.views.generic import View 
from . forms import Register
from . forms import LoginForm
from . forms import AddNoteForm
from . models import Notes

from django.views.generic.base import RedirectView


# Create your views here.

    


class UserHome(View):
    def get(self,request):
        return render(request,'index.html')
        


  

class RegisterView(View):
    def get(self,request):
        form = Register()
        return render(request,'register.html',{'form':form})
    def post(self,request):
        form = Register(request.POST)
        if form.is_valid():
            name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            myuser = User.objects.create_user(username = email,email = email,password = password,first_name = name)
            myuser.save()
            return HttpResponseRedirect('/userlogin/')




class LoginView(View):
    def post(self,request):
        form = LoginForm(request.POST)
        if(form.is_valid()):
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user = authenticate(username = email,password = password)
            if user:
                login(request,user)
                return HttpResponseRedirect('/userprofile/')
            else:
                return HttpResponseRedirect('/userlogin/')
    def get(self,request):
        if not request.user.is_authenticated:  #login nahi hai
            form = LoginForm()
            return render(request,'userlogin.html',{'form':form})
        else:
            return HttpResponseRedirect('/userprofile/')



class UserProfileView(View):
    def get(self,request):
        if request.user.is_authenticated:
            form = AddNoteForm()
            user = User.objects.get(id = request.user.id)
            print(user)
            notes = Notes.objects.filter(user = user)
            print(notes)
            return render(request,'userprofile.html',{'form':form,'notes':notes})
        else:
            return HttpResponseRedirect('/userlogin/')

    def post(self,request):
        form = AddNoteForm(request.POST)
        if(form.is_valid()):
            u = User.objects.filter(username = request.user.username).first()
            title = form.cleaned_data['note_title']
            desc = form.cleaned_data['note_description']
            Notes.objects.create(user = u,note_title = title,note_description= desc)
            form = AddNoteForm()
            return HttpResponseRedirect('/userprofile/')
            
            


class UserProfileLogout(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/userlogin/')



class NotesDeleteView(RedirectView):
    url = '/userprofile/'    #redirect hone ke baad yaha jana chahiye
    def get_redirect_url(self,*args, **kwargs):
        #print(kwargs)   {'id':6}
        del_id = kwargs['id']
        Notes.objects.get(pk = del_id).delete()

        return super().get_redirect_url(*args,**kwargs)



class NotesUpdateView(View):
    def get(self,request,id):
        pi = Notes.objects.get(pk = id)
        fm = AddNoteForm(instance = pi)
        return render(request,'notesupdate.html',{'form':fm})


        
    def post(self,request,id):
        pi = Notes.objects.get(pk = id)
        fm = AddNoteForm(request.POST,instance= pi)
        if fm.is_valid:
            fm.save()
            return HttpResponseRedirect('/userprofile/')

        

"""
 if request.method == 'POST':
        pi = Books.objects.get(pk = id)
        print(pi)
        form = AddpostForm(request.POST,instance=pi)
        form.save()
    else:
        pi = Books.objects.get(pk = id)
        form = AddpostForm(instance=pi)
    return render(request,'updatebook.html',{'form':form})

"""
    




        





