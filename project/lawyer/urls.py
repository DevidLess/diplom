from django.urls import path
from . import views

app_name = 'lawyers'

urlpatterns = [
    path('', views.lawyer_list, name='lawyer_list'),
    path('<int:lawyer_id>/', views.lawyer_detail, name='lawyer_detail'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.confirm_delete_review, name='confirm_delete_review'),  # Новый маршрут
    path('review/<int:review_id>/delete/confirm/', views.delete_review, name='delete_review'),  # Старый маршрут для прямого удаления
]