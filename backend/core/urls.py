from django.urls import path,re_path
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login),
    path('signup/',views.signup),
    path('check_login/',views.check_login),
    path('kich-hoat-tai-khoan/<str:hash_active>/', views.kich_hoat_tai_khoan, name='kich_hoat_tai_khoan')
    # path('kich-hoat-tai-khoan/<int:id>/', views.kich_hoat_tai_khoan),
]

    # path('', views.home, name='home'),
    # path('detail/<int:id>',views.detail_email,name = 'detail_email'),
    # path('search/',views.seach_email,name='seach_email'),
    # path('delete/<int:id>',views.delete_email,name='delete_email'),


