"""simple_votings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from main import views
from simple_votings import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(extra_context={
        'menu': views.get_menu_context(),
        'pagename': 'Авторизация'}),
         name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.registration_page, name='registration'),

    path('registration/college_manager',
         views.registration_store_manager_page,
         name='registration_store_manager'),

    path('', views.catalog_reviews, name='index'),

    path('profile/', views.profile_page, name='profile'),
    path('profile/<int:user_id>/edit/', views.profile_edit_page, name='profile_edit'),
    path('field/add/', views.product_add_page, name='add_product'),
    path('group/add/', views.category_add_page, name='add_category'),
    path('field/delete/<int:product_id>', views.product_delete, name='product_delete'),
    path('category/delete/<int:product_id>', views.category_delete, name='category_delete'),
    path('field/<int:product_id>/edit/', views.product_edit_page, name='product_edit_page'),

    path('catalog_field/', views.catalog_reviews, name='catalog_reviews'),
    path('category/edit/', views.category_edit_page, name='category_edit'),
    path('applications/', views.applications_page, name='applications'),
    path('applications/<int:app_id>/accept', views.application_accept, name='application_accept'),
    path('applications/<int:app_id>/reject', views.application_reject, name='application_reject'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('calc/', views.calc),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('review/<int:id>', views.review_page, name='review_page') - Страница обзора
