from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('update/<int:pk>/', views.update_book, name='update_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('request/<int:pk>/', views.request_book, name='request_book'),
    path('my-requests/', views.view_my_requests, name='my_requests'),
    path('librarian/', views.librarian_dashboard, name='librarian_dashboard'),
    path('librarian/requests/', views.librarian_requests, name='librarian_requests'),
    path('librarian/issued/', views.librarian_issued, name='librarian_issued'),
    path('approve/<int:pk>/', views.approve_request, name='approve_request'),
    path('reject/<int:pk>/', views.reject_request, name='reject_request'),
    path('issue/<int:pk>/', views.issue_book, name='issue_book'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student-books/', views.student_books, name='student_books'),
    path('signup/', views.signup, name='signup'),
]
