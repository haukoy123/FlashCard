from django.urls import path
from Cards import views

app_name = 'cards'

urlpatterns = [
    path('create/<int:pk>/<str:btn>/', views.CreateCard.as_view(), name='create_card'),
    # path('details/<int:pk>/', views.CardDetails.as_view(), name='card_details'),
    path('<int:id_group>/<int:id_card>/update', views.UpdateCard, name='update_card'),
    path('<int:id_group>/<int:id_card>/delete', views.DeleteCard, name='delete_card'),

]