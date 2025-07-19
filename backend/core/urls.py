from django.urls import path,re_path
from .views import view_KhachHang,view_HoSoHocTap



app_name = 'core'

urlpatterns = [
    path('', view_KhachHang.home, name='home'),
    path('login/',view_KhachHang.login),
    path('signup/',view_KhachHang.signup),
    path('check_login/',view_KhachHang.check_login),
    path('logout/',view_KhachHang.logout),
    path('logout-all/',view_KhachHang.logout_all),
    path('kich-hoat-tai-khoan/<str:hash_active>/', view_KhachHang.kich_hoat_tai_khoan, name='kich_hoat_tai_khoan'),

    path('ho-so-hoc-tap/create',view_HoSoHocTap.create_HoSo),
    path('ho-so-hoc-tap/delete/<int:id>/',view_HoSoHocTap.delete_HoSo),
    path('ho-so-hoc-tap/data',view_HoSoHocTap.data_HoSo),
    path('cap-do/data',view_HoSoHocTap.data_CapDo),
    path('ngon-ngu/data',view_HoSoHocTap.data_NgonNgu),
  

]




