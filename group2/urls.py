from django.urls import path
from . import views

urlpatterns = [
    path('select-topic/', views.select_topic, name='select_topic'),
    path('view-lesson/<int:lesson_id>/', views.view_lesson, name='view_lesson'),
    path('complete-exercise/<int:exercise_id>/', views.submit_answer_view, name='complete_exercise'),
    path('search-lesson/', views.search_lesson, name='search_lesson'),
    path('review-progress/<int:user_id>/', views.progress_view, name='review_progress'),
]
