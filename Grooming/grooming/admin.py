from django.contrib import admin
from .models import users_data , shops_data,shop_service


class users_dataAdmin(admin.ModelAdmin):
    list_display = [ 'id','Name','Gender','Email','Contact','Password','Locality',]

class shops_dataAdmin(admin.ModelAdmin):
    list_display = ['id','Name','Gender','Shopname','Service','Email','Contact','Password','Locality',]

class shop_serviceAdmin(admin.ModelAdmin):
    list_display=['id','Email','Service','Price']

admin.site.register(users_data,users_dataAdmin)
admin.site.register(shops_data,shops_dataAdmin)
admin.site.register(shop_service,shop_serviceAdmin)
