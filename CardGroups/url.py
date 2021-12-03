from django.urls import path
from CardGroups import views

app_name = 'cardgroups'

urlpatterns = [
    path('learn/', views.CardGroupView.as_view(), name='learn'),
    path('cardgroups/create', views.CreateGroup.as_view(), name='create_group'),
    # path('cardgroups/details/<int:pk>/', views.GroupDetails.as_view(), name='group_details'),
    # path('cardgroups/<int:pk>/update/', views.UpdateGroup.as_view(), name='update_group'),
    path('cardgroups/details/<int:pk>/', views.UpdateGroup.as_view(), name='group_details'),
    path('cardgroups/<int:pk>/delete/', views.DeleteGroup.as_view(), name='delete_group'),

]