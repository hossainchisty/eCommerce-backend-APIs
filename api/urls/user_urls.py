from django.urls import path
from api.views import user_views as views


urlpatterns = [
    # User management rounter
    path("", views.getUsersList, name="getUserList"),
    # Login & Register router
    path("login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", views.UserCreateView.as_view(), name="register"),
    #
    path("<int:pk>/", views.getUserById, name="user"),
    path("profile/", views.getUserProfile, name="profile"),
    path("update/<int:pk>/", views.updateUser, name="update_user"),
    path("update/profile/", views.updateUserProfile, name="update_profile"),
    path("delete/<int:pk>/", views.deleteUser, name="delete_user"),
    path("deactivate/<int:pk>/", views.deactivateUser, name="deactivate_profile"),
]
