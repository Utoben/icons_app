from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Image(models.Model):
    image = models.ImageField('Изображение', null=True, blank=True, upload_to='images/')
    file  = models.FileField('Документ', null=True, blank=True, upload_to='images/')
    file_name = models.TextField('Имя файла', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now())

    is_choised = models.BooleanField('Выбрано', null=True, blank=True, default=False)

    def __str__(self) -> str:
        return f'{self.file_name} {self.created_at}'

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)
    name = models.TextField('Имя', null=True, blank=True)
    surname = models.TextField('Фамилия', null=True, blank=True)
    patronymic = models.TextField('Отчество', null=True, blank=True)
    phone = models.TextField('Телефон', null=True, blank=True)
    email = models.EmailField('Email', null=True, blank=True)
    agree_to_recieve = models.BooleanField('Согласен получать сообщения', null=True, blank=True, default=True)

    chosen_images = models.ManyToManyField(Image, blank=True, related_name='users', verbose_name='Выбранные значки')

    def __str__(self):
        # return self.user.username 
        return f"{self.name} {self.surname} {self.patronymic}"
    
    def save(self, *args, **kwargs):
        print("Saving user_profile...")
        # slug_text = f'{self.user}'
        # self.user_profile_slug = slugify(slug_text)
        super(UserProfile, self).save(*args, **kwargs)
        print("User_profile saved.")

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'