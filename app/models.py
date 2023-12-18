from django.db import models

from .constants import ARGENTINA, COUNTRY


class ModelSkill(models.Model):
    skill = models.CharField(max_length=100, blank=False, null=True)

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return f'{self.skill}'


class ModelJobPosting(models.Model):
    name = models.CharField(max_length=100, blank=False, null=True)
    salary = models.IntegerField(blank=False, null=True)
    country = models.CharField(
        max_length=100,
        choices=COUNTRY,
        default=ARGENTINA
    )
    skill = models.ManyToManyField(ModelSkill)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'

    def __str__(self):
        return f'{self.name}'


class ModelJobAlert(models.Model):
    email = models.EmailField(max_length=100, blank=False, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(
        max_length=100,
        choices=COUNTRY,
        blank=True,
        null=True
    )
    salary_min = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Job Alert'
        verbose_name_plural = 'Job Alerts'

    def __str__(self):
        return f'{self.email}'
