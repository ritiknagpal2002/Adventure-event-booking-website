from django.urls import path
from . import views
from django.urls import include

app_name = 'myapp1'
urlpatterns = [
    path('', views.login_request, name='login'),
    path('myapp/user-profile/', views.mainpg , name='user_profile'),
    path('myapp/client-profile/', views.clientprofilepg, name='client_profile'),
    path('myapp/homepage/', views.homepage, name='homepage'),
    path('myapp/signup', views.create_client, name='createClient'),
    path('myapp/fp', views.forgot_password, name='forgotpassword'),
    path('myapp/createevent', views.create_event, name='createevent'),
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),
    path('myapp/advanture/<int:type_id>/', views.adventures_by_type, name='adventuresdetail'),
    path('myapp/bookingevent/<int:event_id>/', views.bookevent, name='bookevent'),
    path('myapp/generatepdf/<int:event_id>', views.generatepdf, name='generatepdf'),
    path('myapp/search', views.search, name="search"),
]
