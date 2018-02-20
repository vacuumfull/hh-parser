from django.db import models



class VacancyManager(models.Manager):

    def last(self):
        """All published post."""
        result = Vacancy.objects.order_by('date').reverse()[:10]
        return result


class Vacancy(models.Model):

    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    date = models.DateTimeField(blank=True, null=True,
                                verbose_name='Дата')
        
    link = models.CharField(max_length=200, verbose_name='Ссылка')
    employer = models.CharField(max_length=200, verbose_name='Работодатель')
    salary = models.CharField(max_length=200, verbose_name='Зарплатка')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')
    experience = models.TextField(blank=True, null=True, verbose_name='Опыт')

    objects = VacancyManager()

    def __str__(self):
        return '{} ({})'.format(self.title, self.date)

    class Meta:
        ordering = ['date', 'title']
        verbose_name = 'Вакансии'
        verbose_name_plural = 'Вакансии'

