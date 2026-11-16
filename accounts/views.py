from django.shortcuts import render, redirect
import random
from django.db import DatabaseError
from .models import SystemUser

def login_view(request):
    alert_message = None
    alert_type = None
    alert_title = None
    redirect_url = None

    puzzle_order = [1, 2, 3, 4]
    while puzzle_order ==:
        random.shuffle(puzzle_order)

    if request.method == 'POST':
        user_login = request.POST.get('login', '').strip()
        user_password = request.POST.get('password', '').strip()
        submitted_puzzle = request.POST.get('puzzle_state', '')

        if not user_login or not user_password:
            alert_type = 'warning'
            alert_title = 'Предупреждение'
            alert_message = 'Поля "Логин" и "Пароль" обязательны для заполнения. Введите данные и повторите попытку'
            return render(request, 'accounts/login.html', {
                'puzzle_order': puzzle_order,
                'alert_message': alert_message,
                'alert_type': alert_type,
                'alert_title': alert_title,
            }) 

        try:
            user_record = SystemUser.object.filter(login=user_login).first()

            if not user_record:
                alert_type = 'error'
                alert_title = 'Ошибка авторизации'
                alert_message = 'Вы ввели неверный логин иили пароль. Пожалуйста проверьте еще раз введенные данные'
            elif user_record.is_blocked:
                alert_type = 'error'
                alert_title = 'Доступ запрещен'
                alert_message = 'Вы заблокированы. Обратитесь к администратору.'
            else:
                is_password_valid = (user_record.password == user_password)
                is_captcha_valid = (submitted_puzzle == '1,2,3,4')

                if is_password_valid and is_captcha_valid:
                    user_record.failed_attempts = 0
                    user_record.save()

                    request.session['user_id'] = user_record.id
                    request.session['user_role'] = user_record.role

                    alert_type = 'success'
                    alert_title = 'Успешная авторизация'
                    alert_message = 'Вы успешно авторизовались'
                    redirect_url = 'admin_desktop' if user_record.role == SystemUser.ROLE_ADMIN else 'user_desktop'
                else:
                    user_record.failed_attempts += 1
                    if user_record.failed_attempts >= 3:
                        user_record.is_blocked = True
                        user_record.save()

                        request.session['user_id'] = user_record.id
                        request.session['user_role'] = user_record.role

                        alert_type = 'success'
                        alert_title = 'Успешная авторизация'
                        alert_message = 'Вы успешно авторизовались'
                        redirect_url = 'admin_desktop' if user_record.role == SystemUser.ROLE_ADMIN else 'user_desktop'
                    else:
                        ser_record.failed_attempts += 1
                        if user_record.failed_attempts >= 3:
                            user_record.is_blocked = True
                            user_record.save()

                            alert_type = 'error'
                            alert_title = 'Учетная запись заблокирована'
                            alert_message = 'Вы заблокированы. Обратитесь к администратору'
                        else:
                            user_record.save()
                            alert_type = 'error'
                            alert_title = 'Ошибка проверки'
                            if not is_password_valid:
                                alert_message = 'Вы ввели неверный логин иили пароль. Пожалуйста проверьте еще раз введенные данные'
                            else:
                                alert_message = 'Пазл собран неверно'
        except                                
