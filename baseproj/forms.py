from django.contrib.auth.models import User
from django import forms
from baseproj.models import Notes

class Register(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','email','password')

        widgets = {
            'first_name': forms.TextInput(attrs = {'class':'form-control'}),
            'email':forms.EmailInput(attrs = {'class':'form-control'}),
            'password':forms.PasswordInput(attrs = {'class':'form-control'}),

        }
        

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs = {'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'form-control'}))

class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('note_title','note_description')
        widgets = {
            'note_title': forms.TextInput(attrs = {'class':'form-control','id':'notetitle'}),
            'note_description':forms.TextInput(attrs = {'class':'form-control','id':'notedesc'}),
            

        }



   