from django.urls import path,include
from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView,TokenVerifyView

router = routers.DefaultRouter()
router.register('companies',views.companyview)
router.register('employee',views.employeeview)

urlpatterns = [
    #path('collage-info/',views.collage_list,name="rest-get"),
    #path('collage-updates/<int:pk>/',views.collage_updates,name="c-u"),
    #path('student-info/',views.student_info,name="si"),
    path('',include(router.urls)),
    path('auth/',include('rest_framework.urls')),
    path('user-tokens/',obtain_auth_token),
    path('gettkn/',TokenObtainPairView.as_view()),
    path('refreshtkn/',TokenRefreshView.as_view()),
    path('verifytkn/',TokenVerifyView.as_view()),          # optional
]
