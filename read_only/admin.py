from django.contrib import admin
from models import UserProfile, Tag, Question, Answer, LikeAnswer, LikeQuestion
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

class QuestionAdmin(admin.ModelAdmin):
    pass
    
class AnswerAdmin(admin.ModelAdmin):
    pass
    
class LikeAnswerAdmin(admin.ModelAdmin):
    pass
    
class LikeQuestionAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(LikeAnswer, LikeAnswerAdmin)
admin.site.register(LikeQuestion, LikeQuestionAdmin)
