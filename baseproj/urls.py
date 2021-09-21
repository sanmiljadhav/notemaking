from django.urls import path
from . import views
urlpatterns = [
    path('', views.UserHome.as_view(),name = 'user_home'),
    path('userlogin/',views.LoginView.as_view(),name = 'user_login'),
    path('register/',views.RegisterView.as_view(),name = 'register'),
    path('userprofile/',views.UserProfileView.as_view(),name = 'userprofile'),
    path('logout/',views.UserProfileLogout.as_view(),name = 'userlogout'),
    path('delete/<int:id>',views.NotesDeleteView.as_view(),name = 'notesdelete'),
    path('<int:id>',views.NotesUpdateView.as_view(),name= 'updatedata')
    

    
]
