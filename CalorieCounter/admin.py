from django.contrib import admin
from CalorieCounter.models import *

# Register your models here.
admin.site.register([
    User,
    BasicInfoModel,
    ConsumedCalories,
])