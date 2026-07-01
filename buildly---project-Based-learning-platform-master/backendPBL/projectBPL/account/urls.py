# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterLearnerView,
    RegisterAdminView,
    LoginView,
    LogoutView,
    ProfileView,
    ProfileAvatarDeleteView,
    ChangePasswordView,
    SubmitQuizView
)
from .views_dashboard import (
    LearnerDashboardView,
    LearnerProgressAPIView,
)
from .views_favorites import ListFavoritesView, ToggleFavoriteView
from .views_notifications import (
    ListNotificationsView,
    UnreadNotificationsCountView,
    MarkNotificationReadView,
    MarkAllNotificationsReadView,
    DeleteNotificationView,
    DeleteAllNotificationsView,
)
from .views_email_verification import VerifyEmailView, ResendOTPView
from .views_password_reset import (
    PasswordResetRequestView,
    PasswordResetResendOTPView,
    PasswordResetVerifyOTPView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path('register/learner/', RegisterLearnerView.as_view(), name='register-learner'),
    path('register/admin/', RegisterAdminView.as_view(), name='register-admin'),
    path('verify/confirm/', VerifyEmailView.as_view(), name='verify-email'),
    path('verify/resend/', ResendOTPView.as_view(), name='resend-otp'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/resend/', PasswordResetResendOTPView.as_view(), name='password-reset-resend'),
    path('password-reset/verify-otp/', PasswordResetVerifyOTPView.as_view(), name='password-reset-verify-otp'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/avatar/', ProfileAvatarDeleteView.as_view(), name='profile-avatar-delete'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('quiz/submit/', SubmitQuizView.as_view(), name='submit-quiz'),




     # مسارات لوحة تحكم المتعلم
    path('learner/dashboard/', LearnerDashboardView.as_view(), name='learner-dashboard'),
    path('learner/progress/', LearnerProgressAPIView.as_view(), name='learner-progress'),

    # المفضلة
    path('favorites/', ListFavoritesView.as_view(), name='list-favorites'),
    path('favorites/toggle/', ToggleFavoriteView.as_view(), name='toggle-favorite'),

    # الإشعارات
    path('notifications/', ListNotificationsView.as_view(), name='list-notifications'),
    path('notifications/unread-count/', UnreadNotificationsCountView.as_view(), name='notifications-unread-count'),
    path('notifications/read-all/', MarkAllNotificationsReadView.as_view(), name='notifications-read-all'),
    path('notifications/delete-all/', DeleteAllNotificationsView.as_view(), name='notifications-delete-all'),
    path('notifications/<int:notification_id>/read/', MarkNotificationReadView.as_view(), name='notification-mark-read'),
    path('notifications/<int:notification_id>/', DeleteNotificationView.as_view(), name='notification-delete'),
    ]