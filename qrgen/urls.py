from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_qr, name='create-qr'),
    path('qr/<uuid:pk>/', views.qr_detail, name='qr-detail'),
    path('qr/<uuid:pk>/download/<str:format>/',
         views.download_qr, name='download-qr'),
    path('qr/<uuid:pk>/analytics/', views.analytics, name='qr-analytics'),
    path('qr/<uuid:pk>/delete/', views.delete_qr, name='delete-qr'),
    path('redirect/<str:short_url>/', views.redirect_qr, name='redirect-qr'),
    path('analytics/<uuid:pk>/', views.analytics, name='analytics'),
    path('bulk-upload/', views.bulk_upload, name='bulk-upload'),
    path('bulk-jobs/', views.bulk_jobs, name='bulk-jobs'),

    # HTMX endpoints
    path('qr/preview/', views.qr_preview, name='qr-preview'),
    path('qr/<uuid:pk>/update-url/', views.update_dynamic_url, name='update-url'),
]
