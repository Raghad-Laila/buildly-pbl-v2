from rest_framework import serializers

from .models import PlacementAttempt, PlacementQuestion


class PlacementQuestionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementQuestion
        fields = ['id', 'question', 'options', 'topic', 'difficulty_level']


class PlacementStatusSerializer(serializers.Serializer):
    requires_placement = serializers.BooleanField()
    has_completed = serializers.BooleanField()
    has_in_progress = serializers.BooleanField()
    attempt_id = serializers.IntegerField(allow_null=True)
    ability_score = serializers.FloatField(allow_null=True)
    final_level = serializers.CharField(allow_null=True)
    final_level_display = serializers.CharField(allow_null=True)
    completed_at = serializers.DateTimeField(allow_null=True)
    is_enrolled = serializers.BooleanField()
    course_title = serializers.CharField(allow_null=True, required=False)
    track_slug = serializers.CharField(allow_null=True, required=False)
    track_display_name = serializers.CharField(allow_null=True, required=False)
    topics = serializers.ListField(child=serializers.CharField(), required=False)
    topic_labels = serializers.DictField(required=False)
    skills_description = serializers.CharField(allow_null=True, required=False)


class PlacementStartSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()


class PlacementAnswerSerializer(serializers.Serializer):
    attempt_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    selected_answer = serializers.IntegerField(min_value=0)
    time_ms = serializers.IntegerField(min_value=0, required=False, default=0)


class PlacementReplaceQuestionSerializer(serializers.Serializer):
    attempt_id = serializers.IntegerField()
    question_id = serializers.IntegerField()


class PlacementAttemptSerializer(serializers.ModelSerializer):
    final_level_display = serializers.CharField(
        source='get_final_level_display',
        read_only=True,
    )

    class Meta:
        model = PlacementAttempt
        fields = [
            'id',
            'status',
            'ability_score',
            'final_level',
            'final_level_display',
            'total_questions',
            'started_at',
            'completed_at',
        ]
