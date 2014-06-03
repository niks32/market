from django.db  import models

class GetCallModel(models.Model):
    YEAR_IN_SCHOOL_CHOICES = (
        ('Q1', 'Вопрос 1'),
        ('Q2', 'Вопрос 2'),
        ('Q3', 'Вопрос 3'),
        ('Q4', 'Вопрос 4'),
    )

    name = models.CharField(max_length=30, blank=False)
    phone = models.CharField(max_length=30, blank=False)
    quest = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES, default='Q1', verbose_name="Вопрос")
    date=models.DateTimeField(auto_now_add=True)