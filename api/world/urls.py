from django.urls import path
from . import views

urlpatterns =[
    path('',views.world),
    path('void',views.void),
    path('vault',views.vault),
    path('event',views.event),
    path('invasion',views.invasion),
    path('alert',views.alert),
    
]