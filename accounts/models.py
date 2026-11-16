from django.db import models

class SystemUser(models.Model):
    ROLE_ADMIN = 'Администратор'
    ROLE_USER = 'Пользователь'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Администратор'),
        (ROLE_USER, 'Пользователь'),
    ]

    login = models.CharField(max_length=100, unique=True, verbose_name='Логин')
    password = models.CharField(max_length=128, verbose_name='Пароль')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER, verbose_name='Роль')
    is_blocked = models.CharField(default=False, verbose_name='Заблокирован')
    failed_attempts = models.CharField(default=0, verbose_name='Неудачные попытки')

    class Meta:
        db_table = 'Users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.login} ({self.role})"
