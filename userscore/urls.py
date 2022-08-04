from django.urls import path
from . import views
urlpatterns = [
  
   # path('apicheck/', views.getpost.as_view()),
   # path('apicheck/<int:id>', views.delput.as_view()),
   path('apiusers/', views.users, name="apiusers"),
   path('apicreateuser/', views.create_user, name="apicreateuser"),
   path('apiuserupdate/', views.update_user, name="apiuserupdate"),
   
]
