from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('one_time_registration', one_time_registration, name='one_time_registration'),
    path('testing', testing, name='testing'),
    path('select_table_score', select_table_score, name='select_table_score'),
    path('table_score', table_score, name='table_score'),
    path('calculate_result/', calculate_result, name='calculate_result'),
]
