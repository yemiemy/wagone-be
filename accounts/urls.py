from django.urls import path

from accounts import views

urlpatterns = [
    path(
        "register/",
        views.AccountRegistrationView.as_view(),
        name="create_account",
    ),
    path("login/", views.TokenLoginView.as_view(), name="token_login"),
    path("logout/", views.TokenLogoutView.as_view(), name="token_logout"),
    path(
        "verify/",
        views.AccountVerificationView.as_view(),
        name="account_verify",
    ),
    path(
        "verification-code/regenerate/",
        views.RegenerateVerificationCode.as_view(),
        name="regenerate_verifiction_code",
    ),
    path(
        "update-email/",
        views.UpdateUserAccountEmailView.as_view(),
        name="update_email",
    ),
    path(
        "update-name/",
        views.UpdateUserAccountNameView.as_view(),
        name="update_name",
    ),
    path("delete/", views.AccountDeleteView.as_view(), name="account_delete"),
    path(
        "details/", views.AccountDetailsView.as_view(), name="account_details"
    ),
    path(
        "contacts/", views.UserContactsListView.as_view(), name="user_contacts"
    ),
]
