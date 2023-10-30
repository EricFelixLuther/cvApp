from django.db import models
from django.utils.timezone import now

from cvAppMain.models import RecruitmentProcess


class Question(models.Model):
    text = models.CharField(max_length=64)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('text', )


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    process = models.ForeignKey(RecruitmentProcess, on_delete=models.CASCADE, related_name="recruiter_answers")

    def __str__(self):
        return f'{self.question.text}: {self.text}'


class Benefit(models.Model):
    text = models.CharField(max_length=64)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('text', )


class ProcessLog(models.Model):
    process = models.ForeignKey(RecruitmentProcess, on_delete=models.CASCADE, related_name="process_logs")
    timestamp = models.DateTimeField(blank=True, default=now)
    log = models.TextField()

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M')
