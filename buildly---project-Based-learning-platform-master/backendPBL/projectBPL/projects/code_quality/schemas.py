from rest_framework import serializers


class CodeQualityFileSchema(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False)
    content = serializers.CharField(required=True, allow_blank=True)


class CodeQualityTestSummarySchema(serializers.Serializer):
    total = serializers.IntegerField(required=False, default=0)
    passed = serializers.IntegerField(required=False, default=0)
    failed = serializers.IntegerField(required=False, default=0)


class CodeQualityRequestSchema(serializers.Serializer):
    project_id = serializers.IntegerField(required=True)
    files = CodeQualityFileSchema(many=True, required=True, allow_empty=False)
    test_summary = CodeQualityTestSummarySchema(required=False)


class CodeQualityComplexitySchema(serializers.Serializer):
    time = serializers.CharField(required=True, allow_blank=False)
    space = serializers.CharField(required=True, allow_blank=False)


class CodeQualityResponseSchema(serializers.Serializer):
    """Schema for validating structured code quality review output."""

    score = serializers.IntegerField(required=True, min_value=0, max_value=100)
    summary = serializers.CharField(required=True, allow_blank=False)
    complexity = CodeQualityComplexitySchema(required=True)
    strengths = serializers.ListField(
        child=serializers.CharField(allow_blank=False),
        required=True,
        allow_empty=True,
    )
    clean_code_tips = serializers.ListField(
        child=serializers.CharField(allow_blank=False),
        required=True,
        allow_empty=True,
    )
    performance_tips = serializers.ListField(
        child=serializers.CharField(allow_blank=False),
        required=True,
        allow_empty=True,
    )
