"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mangement_advertiser.views import (ShowAdView, CreateAdView, AdStatisticsView, AdClickView, RegisterUserView,
                                        ProfileUserView, AdvertiserListCreateView, AdvertiserDetailView,
                                        AdListCreateView, AdDetailView,
                                        ClickListCreateView, ClickDetailView,
                                        ViewListCreateView, ViewDetailView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('show_ad/', ShowAdView.as_view()),
    path('ad-statistics/<int:unique_id_ad>/', AdStatisticsView.as_view()),
    path('create_ad/', CreateAdView.as_view(), name='create_ad'),
    path('redirect/<int:pk>/', AdClickView.as_view(), name='ad_click'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
    path('advertisers/', AdvertiserListCreateView.as_view(), name='advertiser-list-create'),
    path('advertisers/<int:pk>/', AdvertiserDetailView.as_view(), name='advertiser-detail'),
    path('ads/', AdListCreateView.as_view(), name='ad-list-create'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    path('clicks/', ClickListCreateView.as_view(), name='click-list-create'),
    path('clicks/<int:pk>/', ClickDetailView.as_view(), name='click-detail'),
    path('views/', ViewListCreateView.as_view(), name='view-list-create'),
    path('views/<int:pk>/', ViewDetailView.as_view(), name='view-detail'),
]
