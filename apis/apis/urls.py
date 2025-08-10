
from django.contrib import admin
from django.urls import path,include
from apapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/',include('apapp.urls')),
    path('',views.homepage),
    path('onlyview/',views.onlyone.as_view(), name="only"),
    path('doubleR/',views.doubleR.as_view(),name="amrin"),
    path('homecbv/',views.homefromcbv.as_view()),
    path('overide/',views.overide.as_view()),
    path('jump/',views.jump.as_view()),
    path('get_col/',views.prac.as_view()),
    path('cre_col/',views.prac_add.as_view()),
    path('revr/',views.revr.as_view()),
    path('1listv/',views.show1list.as_view(),name="parul_added"),
    path('b2list/',views.show2list.as_view()),
    path('stdt/<int:pk>/',views.detail.as_view()),
    path('addst/',views.crev.as_view()),
    path('upd/<int:pk>/',views.updat.as_view()),
    path('del/<int:pk>/',views.delv.as_view()),
    path('api/',include('apapp.urls')),
]
