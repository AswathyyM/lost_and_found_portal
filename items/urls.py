from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('add/', add_item),
    path('claim/<int:id>/', claim),
    path('edit/<int:id>/', edit_item, name='edit_item'),
    path('delete/<int:id>/', delete_item, name='delete_item'),
    path('signup/', signup),
    path(
        'login/',
        UserLoginView.as_view(),
        name='login'
    ),
]
