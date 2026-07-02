# accounts/models.py 
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# **مدير مخصص للمستخدمين بدون اسم مستخدم**
class CustomUserManager(BaseUserManager):
    """مدير مخصص لإنشاء مستخدمين بدون اسم مستخدم"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('يجب إدخال البريد الإلكتروني'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('المشرف يجب أن يكون is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('المشرف يجب أن يكون is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)

# **النموذج المخصص للمستخدمين**
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('learner', 'متعلم'),
        ('admin', 'مشرف'),
    )
    
    username = None  # نحذف حقل اسم المستخدم
    email = models.EmailField(_('البريد الإلكتروني'), unique=True)
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='learner',
        verbose_name='نوع المستخدم'
    )

    is_rated = models.BooleanField(
        default=False,
        verbose_name='هل تم تقييم المستخدم'
    )

    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    )

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        null=True,
        blank=True,
        verbose_name='مستوى المستخدم'
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        verbose_name='الصورة الشخصية',
    )

    email_verified = models.BooleanField(
        default=False,
        verbose_name=_('تم التحقق من البريد الإلكتروني'),
    )
    
    # **حقل جديد: المسارات التعليمية المنضم لها المتعلم (فقط للمتعلمين)**
    enrolled_courses_titles = models.JSONField(
        default=list,
        verbose_name='عناوين المسارات المنضم لها',
        help_text=_('قائمة بعناوين المسارات التي انضم لها المتعلم'),
        blank=True,
        null=True  # السماح بقيمة فارغة للمشرفين
    )

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 
    
    def __str__(self):
        return self.email
    
    def get_user_type_display(self):
        """إرجاع النص المعروض لنوع المستخدم"""
        for value, label in self.USER_TYPE_CHOICES:
            if value == self.user_type:
                return label
        return self.user_type
    
    @property
    def is_learner(self):
        return self.user_type == 'learner'
    
    @property
    def is_admin(self):
        return self.user_type == 'admin' or self.is_superuser
    
    # **دالة جديدة: إضافة مسار للمتعلم**
    def add_enrolled_course(self, course_title):
        """إضافة عنوان مسار إلى قائمة المسارات المنضم لها"""
        if self.is_learner:
            # تهيئة القائمة إذا كانت فارغة
            if self.enrolled_courses_titles is None:
                self.enrolled_courses_titles = []
            
            if course_title not in self.enrolled_courses_titles:
                self.enrolled_courses_titles.append(course_title)
                self.save()
                print(f" تم إضافة المسار '{course_title}' للمتعلم '{self.email}'")
                return True
            else:
                print(f" المسار '{course_title}' موجود بالفعل في قائمة المتعلم '{self.email}'")
                return False
        print(f" المستخدم '{self.email}' ليس متعلمًا")
        return False
    
    # **دالة جديدة: إزالة مسار من قائمة المتعلم**
    def remove_enrolled_course(self, course_title):
        """إزالة عنوان مسار من قائمة المسارات المنضم لها"""
        if self.is_learner and self.enrolled_courses_titles and course_title in self.enrolled_courses_titles:
            self.enrolled_courses_titles.remove(course_title)
            self.save()
            print(f" تم إزالة المسار '{course_title}' من قائمة المتعلم '{self.email}'")
            return True
        return False
    
    # **دالة جديدة: التحقق من انضمام المتعلم للمسار**
    def is_enrolled_in_course(self, course_title):
        """التحقق إذا كان المتعلم منضم لمسار معين"""
        return self.is_learner and self.enrolled_courses_titles and course_title in self.enrolled_courses_titles
    
    # **دالة جديدة: الحصول على عدد المسارات المنضم لها المتعلم**
    def get_enrolled_courses_count(self):
        """الحصول على عدد المسارات المنضم لها"""
        if self.is_learner and self.enrolled_courses_titles:
            return len(self.enrolled_courses_titles)
        return 0
    
    # **دالة جديدة: عرض قائمة المسارات المنضم لها المتعلم**
    def get_enrolled_courses_list(self):
        """الحصول على قائمة المسارات المنضم لها"""
        if self.is_learner and self.enrolled_courses_titles:
            return self.enrolled_courses_titles
        return []
    
    # **حفظ النموذج مع ضبط القيم للمشرفين**
    def save(self, *args, **kwargs):
        # للمشرفين، نضع enrolled_courses_titles كـ None
        if self.user_type == 'admin' and self.enrolled_courses_titles:
            self.enrolled_courses_titles = None
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمين')


class UserFavorite(models.Model):
    """مفضلة المستخدم للمسارات والمشاريع"""

    ITEM_TYPE_COURSE = 'course'
    ITEM_TYPE_PROJECT = 'project'
    ITEM_TYPE_CHOICES = (
        (ITEM_TYPE_COURSE, _('مسار')),
        (ITEM_TYPE_PROJECT, _('مشروع')),
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_('المستخدم'),
    )
    item_type = models.CharField(
        max_length=10,
        choices=ITEM_TYPE_CHOICES,
        verbose_name=_('نوع العنصر'),
    )
    object_id = models.PositiveIntegerField(verbose_name=_('معرف العنصر'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإضافة'))

    class Meta:
        verbose_name = _('مفضلة')
        verbose_name_plural = _('المفضلة')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'item_type', 'object_id'],
                name='unique_user_favorite_item',
            )
        ]

    def __str__(self):
        return f'{self.user.email} - {self.item_type} #{self.object_id}'


class Notification(models.Model):
    """إشعارات داخل النظام للمستخدمين"""

    TYPE_ACCOUNT_CREATED = 'account_created'
    TYPE_PROJECT_STARTED = 'project_started'
    TYPE_PROJECT_SUBMITTED = 'project_submitted'
    TYPE_PROJECT_GRADED = 'project_graded'
    TYPE_PASSWORD_RESET = 'password_reset'
    TYPE_CHOICES = (
        (TYPE_ACCOUNT_CREATED, _('إنشاء حساب')),
        (TYPE_PROJECT_STARTED, _('بدء مشروع')),
        (TYPE_PROJECT_SUBMITTED, _('استلام مشروع')),
        (TYPE_PROJECT_GRADED, _('تقييم مشروع')),
        (TYPE_PASSWORD_RESET, _('إعادة تعيين كلمة المرور')),
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('المستخدم'),
    )
    title = models.CharField(max_length=200, verbose_name=_('العنوان'))
    message = models.TextField(verbose_name=_('الرسالة'))
    notification_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default=TYPE_PROJECT_GRADED,
        verbose_name=_('نوع الإشعار'),
    )
    is_read = models.BooleanField(default=False, verbose_name=_('مقروء'))
    related_project_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('معرف المشروع المرتبط'),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))

    class Meta:
        verbose_name = _('إشعار')
        verbose_name_plural = _('الإشعارات')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.title}'


class EmailVerificationOTP(models.Model):
    """رمز تحقق البريد الإلكتروني عند إنشاء الحساب"""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='email_otps',
        verbose_name=_('المستخدم'),
    )
    code_hash = models.CharField(max_length=128, verbose_name=_('رمز التحقق المشفر'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    expires_at = models.DateTimeField(verbose_name=_('تاريخ انتهاء الصلاحية'))
    is_used = models.BooleanField(default=False, verbose_name=_('مستخدم'))

    class Meta:
        verbose_name = _('رمز تحقق البريد')
        verbose_name_plural = _('رموز تحقق البريد')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_used', 'created_at']),
        ]

    def __str__(self):
        return f'{self.user.email} - OTP #{self.id}'

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() >= self.expires_at


class PasswordResetOTP(models.Model):
    """رمز تحقق إعادة تعيين كلمة المرور"""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='password_reset_otps',
        verbose_name=_('المستخدم'),
    )
    code_hash = models.CharField(max_length=128, verbose_name=_('رمز التحقق المشفر'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    expires_at = models.DateTimeField(verbose_name=_('تاريخ انتهاء الصلاحية'))
    is_used = models.BooleanField(default=False, verbose_name=_('مستخدم'))

    class Meta:
        verbose_name = _('رمز إعادة تعيين كلمة المرور')
        verbose_name_plural = _('رموز إعادة تعيين كلمة المرور')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_used', 'created_at']),
        ]

    def __str__(self):
        return f'{self.user.email} - reset OTP #{self.id}'

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() >= self.expires_at


class PasswordResetSession(models.Model):
    """جلسة آمنة لإعادة تعيين كلمة المرور بعد التحقق من OTP"""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='password_reset_sessions',
        verbose_name=_('المستخدم'),
    )
    token_hash = models.CharField(max_length=128, verbose_name=_('رمز الجلسة المشفر'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    expires_at = models.DateTimeField(verbose_name=_('تاريخ انتهاء الصلاحية'))
    is_used = models.BooleanField(default=False, verbose_name=_('مستخدم'))

    class Meta:
        verbose_name = _('جلسة إعادة تعيين كلمة المرور')
        verbose_name_plural = _('جلسات إعادة تعيين كلمة المرور')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_used', 'expires_at']),
        ]

    def __str__(self):
        return f'{self.user.email} - reset session #{self.id}'

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() >= self.expires_at