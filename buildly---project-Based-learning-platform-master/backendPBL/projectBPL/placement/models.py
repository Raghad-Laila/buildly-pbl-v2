from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import DIFFICULTY_LEVELS, FINAL_LEVELS, TOPICS
from .track_config import PLACEMENT_TRACKS


def _topic_label(topic: str) -> str:
    for track in PLACEMENT_TRACKS.values():
        if topic in track['topic_labels']:
            return track['topic_labels'][topic]
    return topic.upper()


class PlacementQuestion(models.Model):
    SOURCE_CHOICES = (
        ('manual', _('يدوي')),
        ('ai', _('ذكاء اصطناعي')),
    )
    TRACK_CHOICES = tuple((slug, config['display_name']) for slug, config in PLACEMENT_TRACKS.items())
    TOPIC_CHOICES = tuple((topic, _topic_label(topic)) for topic in TOPICS)

    question = models.TextField(verbose_name=_('السؤال'))
    options = models.JSONField(verbose_name=_('الخيارات'))
    correct_answer = models.PositiveSmallIntegerField(
        verbose_name=_('رقم الإجابة الصحيحة'),
        help_text=_('فهرس الخيار الصحيح يبدأ من 0'),
    )
    explanation = models.TextField(verbose_name=_('الشرح'))
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES, verbose_name=_('الموضوع'))
    track_slug = models.CharField(
        max_length=20,
        choices=TRACK_CHOICES,
        default='frontend',
        verbose_name=_('المسار'),
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        verbose_name=_('مستوى الصعوبة'),
    )
    difficulty_score = models.FloatField(verbose_name=_('درجة الصعوبة'))
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='manual',
        verbose_name=_('المصدر'),
    )
    attempt = models.ForeignKey(
        'PlacementAttempt',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='generated_questions',
        verbose_name=_('المحاولة'),
    )
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
    random_seed = models.PositiveIntegerField(
        default=0,
        verbose_name=_('بذرة عشوائية'),
        help_text=_('بذرة فريدة لكل محاولة لاختيار أسئلة مختلفة بين الطلاب'),
    )
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
