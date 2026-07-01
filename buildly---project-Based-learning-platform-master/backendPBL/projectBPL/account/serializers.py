# accounts/serializers.py - النسخة المحدثة الكاملة
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import CustomUser

# **سيريالايزر جديد لتسجيل المتعلمين**
class RegisterLearnerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password],style={'input_type': 'password'},min_length=8)
    password2 = serializers.CharField(write_only=True,required=True,style={'input_type': 'password'})
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2', )
    
    # التحقق من البيانات المدخلة من المستخدم validate
    def validate(self, attrs):
        #التحقق من تطابق كلمات المرور
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": ("كلمات المرور غير متطابقة")}
            )
        # التحقق من البريد الإلكتروني validate_email
        try:
            validate_email(attrs['email'])
        except ValidationError:
            raise serializers.ValidationError(
                {"email": ("البريد الإلكتروني غير صالح")}
            )
        # التحقق من وجود البريد مسبقاً
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": ("البريد الإلكتروني موجود مسبقاً")}
            )
        # إزالة تأكيد كلمة المرور من البيانات
        attrs.pop('password2')
        # تعيين نوع المستخدم كمتعلم
        attrs['user_type'] = 'learner'
        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

# **سيريالايزر جديد لتسجيل المشرفين**
class RegisterAdminSerializer(serializers.ModelSerializer):
    """سيريالايزر خاص بإنشاء المشرفين """
    # **حقول كلمة المرور وتأكيدها**
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        min_length=8
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2', )
    
    #تحقق من البيانات المدخلة من المستخدم
    def validate(self, attrs):
        # التحقق من تطابق كلمات المرور
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": ("كلمات المرور غير متطابقة")}
            )
        # التحقق من البريد الإلكتروني
        try:
            validate_email(attrs['email'])
        except ValidationError:
            raise serializers.ValidationError(
                {"email": ("البريد الإلكتروني غير صالح")}
            )
        # التحقق من وجود البريد مسبقاً
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": ("البريد الإلكتروني موجود مسبقاً")}
            )
        # إزالة تأكيد كلمة المرور من البيانات
        attrs.pop('password2')
        # تعيين نوع المستخدم كمشرف
        attrs['user_type'] = 'admin'
        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

# **سيريالايزر جديد لتسجيل الدخول**
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    # التحقق من بيانات الدخول
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        # التحقق من وجود البيانات
        if not email or not password:
            raise serializers.ValidationError(
                ("يجب إدخال البريد الإلكتروني وكلمة المرور")
            )
        # التحقق من البريد الإلكتروني
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError(
                {"email": ("البريد الإلكتروني غير صالح")}
            )
        
        # المصادقة
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError(
                ("بيانات الدخول غير صحيحة")
            )
        if not user.is_active:
            raise serializers.ValidationError(
                ("الحساب غير مفعل")
            )
        attrs['user'] = user
        return attrs

# **سيريالايزر جديد لعرض وتحديث ملف المستخدم**
class ProfileSerializer(serializers.ModelSerializer):
    enrolled_courses_count = serializers.SerializerMethodField()
    enrolled_courses_titles = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'profile_picture',
            'profile_picture_url',
            'user_type',
            'date_joined',
            'last_login',
            'enrolled_courses_count',
            'enrolled_courses_titles',
            'is_rated',
            'level',
        )
        read_only_fields = (
            'id',
            'user_type',
            'date_joined',
            'last_login',
            'profile_picture_url',
            'full_name',
        )
        extra_kwargs = {
            'profile_picture': {'write_only': True, 'required': False, 'allow_null': True},
        }

    def get_profile_picture_url(self, obj):
        if not obj.profile_picture:
            return None

        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return obj.profile_picture.url

    def get_full_name(self, obj):
        full_name = f'{obj.first_name or ""} {obj.last_name or ""}'.strip()
        return full_name or obj.email

    def validate_email(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(('البريد الإلكتروني موجود مسبقاً'))
        return value

    def validate_profile_picture(self, value):
        if value is None:
            return value

        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('حجم الصورة يجب أن لا يتجاوز 5 ميغابايت')

        valid_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
        if getattr(value, 'content_type', None) not in valid_types:
            raise serializers.ValidationError('نوع الصورة غير مدعوم. استخدم JPG أو PNG أو WEBP أو GIF')

        return value

    def update(self, instance, validated_data):
        new_picture = validated_data.get('profile_picture', serializers.empty)

        if new_picture is not serializers.empty and instance.profile_picture:
            instance.profile_picture.delete(save=False)

        return super().update(instance, validated_data)

    def get_enrolled_courses_count(self, obj):
        if obj.is_learner:
            return obj.get_enrolled_courses_count()
        return None

    def get_enrolled_courses_titles(self, obj):
        if obj.is_learner:
            return obj.get_enrolled_courses_list()
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_type'] = instance.get_user_type_display()
        if representation.get('enrolled_courses_count') is None:
            representation.pop('enrolled_courses_count', None)
        if representation.get('enrolled_courses_titles') is None:
            representation.pop('enrolled_courses_titles', None)
        return representation


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=8,
    )
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('كلمة المرور الحالية غير صحيحة')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {'new_password': 'كلمات المرور الجديدة غير متطابقة'}
            )
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user