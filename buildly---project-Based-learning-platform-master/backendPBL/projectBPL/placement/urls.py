from django.urls import path

from .views import (
    FrontendPlacementStartView,
    FrontendPlacementStatusView,
    FrontendPlacementSubmitAnswerView,
    PlacementReplaceQuestionView,
    PlacementStartView,
    PlacementStatusView,
    PlacementSubmitAnswerView,
)

urlpatterns = [
    path(
        'status/<int:course_id>/',
        PlacementStatusView.as_view(),
        name='placement-status',
    ),
    path(
        'start/',
        PlacementStartView.as_view(),
        name='placement-start',
    ),
    path(
        'submit-answer/',
        PlacementSubmitAnswerView.as_view(),
        name='placement-submit-answer',
    ),
    path(
        'replace-question/',
        PlacementReplaceQuestionView.as_view(),
        name='placement-replace-question',
    ),
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
    path(
        'frontend/replace-question/',
        PlacementReplaceQuestionView.as_view(),
        name='frontend-placement-replace-question',
    ),
]
