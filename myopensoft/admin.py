from django.contrib import admin
from .models import Employee,Award,Leave,DailyActivity,Review_Performance,Mood

admin.site.register(Employee)
admin.site.register(Award)
admin.site.register(Leave)
admin.site.register(DailyActivity)
admin.site.register(Review_Performance)
admin.site.register(Mood)
