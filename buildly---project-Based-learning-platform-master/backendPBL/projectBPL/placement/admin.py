from django.contrib import admin

from .models import PlacementAttempt, PlacementQuestion


@admin.register(PlacementQuestion)
class PlacementQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'topic',
        'difficulty_level',
        'difficulty_score',
        'is_active',
        'question_preview',
    )
    list_filter = ('topic', 'difficulty_level', 'is_active')
    search_fields = ('question', 'explanation')

    def question_preview(self, obj):
        return obj.question[:80]


@admin.register(PlacementAttempt)
class PlacementAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'course',
        'status',
        'ability_score',
        'final_level',
        'completed_at',
    )
    list_filter = ('status', 'final_level', 'course')
    search_fields = ('user__email', 'course__title')
