from django.urls import path

from .views import (
    FrontendPlacementStartView,
    FrontendPlacementStatusView,
    FrontendPlacementSubmitAnswerView,
)

urlpatterns = [
    path(
        'frontend/status/<int:course_id>/',
        FrontendPlacementStatusView.as_view(),
        name='frontend-placement-status',
    ),
    path(
        'frontend/start/',
        FrontendPlacementStartView.as_view(),
        name='frontend-placement-start',
    ),
    path(
        'frontend/submit-answer/',
        FrontendPlacementSubmitAnswerView.as_view(),
        name='frontend-placement-submit-answer',
    ),
]
