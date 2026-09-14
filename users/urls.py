from django.urls import path
from .views import SigUpView, LoginView, ProfileView, LogoutView

urlpatterns = [
    path('signup/', SigUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('logout/', LogoutView.as_view()),
    

]