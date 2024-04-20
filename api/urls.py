
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView

# Use TokenRefreshView provided by Simple JWT
refresh_jwt_token = TokenRefreshView.as_view()
urlpatterns = [
    
    #auth
    path('login/',views.login_view , name="Login-Profile"),
    path('register/',views.register_view , name="Register-Profile"),
    path('token/refresh/', refresh_jwt_token, name='token_refresh'),
    
    
    #CRUD Formation
    path('formation/',views.get_Formations , name="Formations"),
    path('formation/<str:id>/' , views.get_Formation , name="Formation"),
    
    
    path('subscribe/<str:id>/' , views.subscribe , name="Subscribe"),
    path('subscribes/',views.get_my_formations , name="My-Formations" ),
    path('delete_subscribe/<int:id>',views.undo_subscribtion , name="Undo-Subscripton")
    
    
    
    
]



