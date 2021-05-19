from django.urls import path
from grooming.views import user_login, user_reg ,shop_reg ,shop_login,home, shop_ui,shop_logout,shop_services,user_service_interface,test

urlpatterns = [

    path('', home,name='home'),
    path('user_login',user_login,name='user_login'),
    path('user_reg/',user_reg,),
    path('shop/',shop_ui,name='shop_ui'),
    path('shop_login',shop_login,name='shop_login'),
    path('shop_reg',shop_reg,name='shop_reg'),
    path('shop_logout',shop_logout,name="shop_logout"),
    path('shop_services',shop_services,name='shop_services'),
    path('service',user_service_interface,name='service'),
    path('test',test,name='test')



]
