from django.urls import path
from Cards import views

app_name = 'cards'

urlpatterns = [
    path('create/<int:pk>/<str:btn>/', views.CreateCard.as_view(), name='create_card'),
    path('details/<int:pk>/', views.CardDetails.as_view(), name='card_details'),

]