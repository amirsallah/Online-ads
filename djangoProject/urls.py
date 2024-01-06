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
from mangement_advertiser.views import ShowAdView, CreateAdView, AdStatisticsView, AdClickView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('show_ad/', ShowAdView.as_view()),
    path('ad-statistics/<int:unique_id_ad>/', AdStatisticsView.as_view()),
    path('create_ad/', CreateAdView.as_view(), name='create_ad'),
    path('redirect/<int:pk>/', AdClickView.as_view(), name='ad_click'),
]
