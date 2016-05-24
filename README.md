# Требования
Python 3
Supervisor - для демонизации gunicorn
Nginx - для раздачи статики 


# Запуск сервера разработчика
1. source ../env/bin/activate - активация окружения
2. python manage.py runserver 0.0.0.0:8000 - запуск веб сервера
3. celery -A conf.app_celery worker -l info -B - запуск воркеров


# Подготовка Вконтакте
Перед инсталяцией необходимо зарегистрировать «Standalone-приложение» Вконтакте https://vk.com/editapp?act=create

Затем используем ссылку
https://oauth.vk.com/authorize?client_id={APP_ID}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall&response_type=token
для получения прав доступа на пост на стены.

ВНИМАНИЕ: VK имеет ограничение в 50 репостов в день.
