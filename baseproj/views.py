from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.views.generic import View 
from . forms import Register
from . forms import LoginForm
from . forms import AddNoteForm
from . models import Notes, SharedWith

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

        

#for sharing notes to other users
class SharePostView(View):
    def get(self,request,id):
        allusers=User.objects.exclude(username = request.user.username)
        return render(request,'searchuser.html',{'context':allusers})
    def post(self,request,id):
        email = request.POST.get('email')
        user = User.objects.filter(username = email).first()   #sending user
        print(user)
        
        if user:
            print("sanmil")
            #currrent
            notes = Notes.objects.get(id = id)
            noteid=notes.id
           
            
            u=User.objects.filter(username = request.user.username).first()   #current user
            SharedWith.objects.create(user = u,shared_user_id = user,noteid = noteid)
            print("note shared")

        return HttpResponseRedirect('/userprofile/')


"""
 u = User.objects.filter(username = request.user.username).first()
            title = form.cleaned_data['note_title']
            desc = form.cleaned_data['note_description']
            Notes.objects.create(user = u,note_title = title,note_description= desc)
            form = AddNoteForm()
            return HttpResponseRedirect('/userprofile/')
"""
        

#sharewith me se logged in user ke shared notes ki id nikali and uske baad notes me se usi id ka data nikal ke populate 
class SharedNotesView(View):
    def get(self,request):
        if request.user.is_authenticated:
            user = User.objects.get(id = request.user.id)  #gives username
            print(user)
            notes = SharedWith.objects.filter(shared_user_id = user).values()
            print(notes)
            lista = []
            for note in notes:
                lista.append(note['noteid'])
            print(lista)
            notea=Notes.objects.filter(id__in=lista)
            print(notea)
            return render(request,'sharednotes.html',{'notes':notea})
        else:
            return HttpResponseRedirect('/userlogin/')

    




