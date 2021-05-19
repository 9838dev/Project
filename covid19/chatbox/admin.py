from django.contrib import admin
from .models import user,feed,feed_answer,Trade_feed,raise_issue,feedback
# Register your models here.
class userAdmin(admin.ModelAdmin):
    list_display = [ 'id','Name','Email','Phone','State','City','Password']

class feedAdmin(admin.ModelAdmin):
    list_display = ['id','Query_box','Email','Raise']

class feed_answerAdmin(admin.ModelAdmin):
    list_display = ['id','Query_Id','Comment']

class Trade_feedAdmin(admin.ModelAdmin):
    list_display = ['id','Email','Trade']

class raise_issueAdmin(admin.ModelAdmin):
    list_display = ['id','Raise_Id','Email']

class feedbackAdmin(admin.ModelAdmin):
    list_display = ['id','Feedback','Email']



admin.site.register(user,userAdmin)
admin.site.register(feed,feedAdmin)
admin.site.register(feed_answer,feed_answerAdmin)
admin.site.register(Trade_feed,Trade_feedAdmin)
admin.site.register(raise_issue,raise_issueAdmin)
admin.site.register(feedback,feedbackAdmin)
