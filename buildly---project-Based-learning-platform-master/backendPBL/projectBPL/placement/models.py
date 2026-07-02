from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import DIFFICULTY_LEVELS, FINAL_LEVELS, TOPICS


class PlacementQuestion(models.Model):
    TOPIC_CHOICES = tuple((topic, topic.upper()) for topic in TOPICS)

    question = models.TextField(verbose_name=_('السؤال'))
    options = models.JSONField(verbose_name=_('الخيارات'))
    correct_answer = models.PositiveSmallIntegerField(
        verbose_name=_('رقم الإجابة الصحيحة'),
        help_text=_('فهرس الخيار الصحيح يبدأ من 0'),
    )
    explanation = models.TextField(verbose_name=_('الشرح'))
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES, verbose_name=_('الموضوع'))
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        verbose_name=_('مستوى الصعوبة'),
    )
    difficulty_score = models.FloatField(verbose_name=_('درجة الصعوبة'))
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['topic', 'difficulty_score', 'id']
        verbose_name = _('سؤال تحديد مستوى')
        verbose_name_plural = _('بنك أسئلة تحديد المستوى')

    def __str__(self):
        return f'[{self.topic}] {self.question[:60]}'


class PlacementAttempt(models.Model):
    STATUS_CHOICES = (
        ('in_progress', _('قيد التنفيذ')),
        ('completed', _('مكتمل')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='placement_attempts',
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='placement_attempts',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    ability_score = models.FloatField(default=0.0)
    final_level = models.CharField(
        max_length=20,
        choices=FINAL_LEVELS,
        null=True,
        blank=True,
    )
    asked_question_ids = models.JSONField(default=list, blank=True)
    responses = models.JSONField(default=list, blank=True)
    total_questions = models.PositiveSmallIntegerField(default=12)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']
        verbose_name = _('محاولة اختبار تحديد مستوى')
        verbose_name_plural = _('محاولات اختبار تحديد المستوى')

    def __str__(self):
        return f'{self.user.email} - {self.course.title} ({self.status})'

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def questions_answered(self):
        return len(self.responses)
