from rest_framework import serializers


class AIReviewFileSchema(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False)
    content = serializers.CharField(required=True, allow_blank=True)


class AIReviewTestSummarySchema(serializers.Serializer):
    total = serializers.IntegerField(required=False, default=0)
    passed = serializers.IntegerField(required=False, default=0)
    failed = serializers.IntegerField(required=False, default=0)


class AIReviewFailedTestSchema(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_blank=True, default='')
    requirement = serializers.CharField(required=False, allow_blank=True, default='')
    message = serializers.CharField(required=False, allow_blank=True, default='')
    error = serializers.CharField(required=False, allow_blank=True, default='')
    stderr = serializers.CharField(required=False, allow_blank=True, default='')


class AIReviewRequestSchema(serializers.Serializer):
    project_id = serializers.IntegerField(required=True)
    files = AIReviewFileSchema(many=True, required=True, allow_empty=False)
    test_summary = AIReviewTestSummarySchema(required=False)
    failed_tests = AIReviewFailedTestSchema(many=True, required=False)
    test_error = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class AIReviewIssueSchema(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    category = serializers.CharField(required=True, allow_blank=False)
    severity = serializers.CharField(required=True, allow_blank=False)
    file = serializers.CharField(required=True, allow_blank=False)
    line = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True, allow_blank=False)
    explanation = serializers.CharField(required=True, allow_blank=False)
    hint = serializers.CharField(required=True, allow_blank=False)


class AIReviewResponseSchema(serializers.Serializer):
    """Schema for validating structured AI review output."""

    overall_score = serializers.IntegerField(required=True)
    summary = serializers.CharField(required=True, allow_blank=False)
    strengths = serializers.ListField(
        child=serializers.CharField(allow_blank=False),
        required=True,
        allow_empty=True,
    )
    issues = AIReviewIssueSchema(many=True, required=True, allow_empty=True)
