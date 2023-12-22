from django.urls import path, include
from rest_framework import routers
from loanapp import views


router = routers.DefaultRouter()
router.register(r'api/users', views.UserViewSet)
router.register(r'api/accounts', views.AccountViewSet)
router.register(r'api/loanplans', views.LoanPlanViewSet)
router.register(r'api/loantypes', views.LoanTypeViewSet)
router.register(r'api/loans', views.LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', views.LoginView.as_view()),
    path('api/logout/', views.LogoutView.as_view()),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('api/user/update-password/', views.update_user_password, name='update_user_password'),
]