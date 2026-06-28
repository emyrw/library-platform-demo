from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Reader
    path('catalogue/', views.catalogue, name='catalogue'),
    path('my-loans/', views.reader_dashboard, name='reader_dashboard'),

    # Librarian
    path('librarian/', views.search_readers, name='search_readers'),
    path('librarian/loan/new/', views.register_loan, name='register_loan'),
    path('librarian/loan/<int:loan_id>/return/', views.register_return, name='register_return'),
        path('librarian/loan/<int:loan_id>/extend/', views.extend_loan, name='extend_loan'),
    path('librarian/readers/<int:reader_id>/loans/', views.reader_loans, name='reader_loans'),
]
