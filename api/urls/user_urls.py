from api.views import user_views as views
from django.urls import path
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    # User management rounter
    path("", views.getUsersList, name="getUserList"),
    # JWT router
    path(
        "api/token/obtain/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_create",
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    # Login & Register router
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    # User profile management router
    path("<int:pk>/", views.getUserById, name="user"),
    path("profile/", views.getUserProfile, name="profile"),
    path("update/<int:pk>/", views.updateUser, name="update_user"),
    path("update/profile/", views.updateUserProfile, name="update_profile"),
    path("delete/<int:pk>/", views.deleteUser, name="delete_user"),
    path("deactivate/<int:pk>/", views.deactivateUser, name="deactivate_profile"),
]
