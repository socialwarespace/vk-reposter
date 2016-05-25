# Требования
Python 3

Supervisor - для демонизации gunicorn

Nginx - для раздачи статики

Redis - Необходим для управления задачами Celery


# Запуск сервера
Для запуска сервера используется [Supervisor](http://supervisord.org/).
При старте сервера демон супервизора автоматически запустит необходимые процессы.

```sudo supervisorctl status - отображает состояние процессов```

```sudo supervisorctl restart reposter: - рестартует проект```


# Настройка приложения

## Подготовка Вконтакте
Перед инсталяцией необходимо зарегистрировать «Standalone-приложение» Вконтакте https://vk.com/editapp?act=create

Затем используем ссылку
https://oauth.vk.com/authorize?client_id={APP_ID}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall&response_type=token
для получения прав доступа на пост на стены.

ВНИМАНИЕ: VK имеет ограничение в 50 репостов в день.

## Конфигурация
Перед работой с приложением необходимо произвести его конфигурацию в файле
```/home/reposter/vk_reposter/src/conf/settings_local.py```

Редактировать файл можно любым текстовым редактором, например nano
```nano /home/reposter/vk_reposter/src/conf/settings_local.py```

Каждый параметр конфигурационного файла документирован и не нуждается в более детальном описании

По умолчанию приложение запускает парсинг и репостинг один раз в час

ВНИМАНИЕ: Что бы изменения в конфигурации вступили в силу необходимо рестартовать приложение
```sudo supervisorctl restart reposter:```

## Интерфейс администратора
Система имеет [интерфейс администратора](http://grigory.keeper.fvds.ru/).
Авторизация осуществляется по логину и паролю.

Паблики для парса необходимо добавлять в разделе [Паблики](http://grigory.keeper.fvds.ru/reposter/public/)

Спарсенные для репоста посты можно видеть в разделе [Посты](http://grigory.keeper.fvds.ru/reposter/post/)
