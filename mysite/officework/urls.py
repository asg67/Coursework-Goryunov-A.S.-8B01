from django.urls import path

from .views import *

urlpatterns = [
    path('', ProjectHome.as_view(), name='home'),
    path('addpage', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    # path('AreaPersonal/', AreaPersonal.as_view(), name='AreaPersonal'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', ProjectCategory.as_view(), name='category')
]

