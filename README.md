# Настройка приложения VK Reposter

## Подготовка Вконтакте
Перед инсталяцией необходимо зарегистрировать «Standalone-приложение» Вконтакте https://vk.com/apps?act=manage.
Необходимо запомнить "ID приложения".

Затем используем ссылку
https://oauth.vk.com/authorize?client_id={APP_ID}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall&response_type=token
для получения прав доступа на пост на стены. Вместо {APP_ID} необходимо подставить "ID приложения".
Необходимо разрешить приложению публиковать посты.

ВНИМАНИЕ: VK имеет ограничение в 50 репостов в день.


## Конфигурация
**Перед работой с приложением необходимо произвести его конфигурацию в разделе [Настройки](http://grigory.keeper.fvds.ru/constance/config/).**

Каждый параметр конфигурационного файла документирован и не нуждается в более детальном описании.

По умолчанию приложение парсит паблики один раз в час, а репост запускается каждые пол часа. 
Если необходимо изменить частоту запуска нужно отредактировать файл конфигурации прилоежния **settings_local.py**.
Редактировать файл можно любым текстовым редактором, например nano.

```nano /home/reposter/vk_reposter/src/conf/settings_local.py```

ВНИМАНИЕ: Что бы изменения в конфигурации вступили в силу необходимо рестартовать приложение
```sudo supervisorctl restart reposter:```


## Интерфейс администратора
Система имеет [Интерфейс администратора](http://grigory.keeper.fvds.ru/), через который можно мониторить работу системы и осуществлять её конфигурацию.
Что бы попасть в админку, необходимо пройти авторизацию по логину и паролю.

### Добавление паблика
Паблики для парса необходимо добавлять в разделе [Паблики](http://grigory.keeper.fvds.ru/reposter/public/).
Что бы добавить новый паблик нужно нажать кнопку **Добавить Паблик** и скопировать полную ссылку на паблик в поле "Адрес паблика".
Паблики должны иметь полный путь, например https://vk.com/it_61.

### Посты
Спарсенные для репоста посты можно видеть в разделе [Посты](http://grigory.keeper.fvds.ru/reposter/post/). 
Посты, репос которых уже был произведён имеют зелёный флаг "Репост сделан".

### Создание нового пользователя
Если необходимо создать нового пользователя для доступа к системе, это можно сделать в разделе [Пользователи](http://grigory.keeper.fvds.ru/auth/user/).
Поскольку интерфейс релазиован через админку Django, после создания пользователя требуется поставить галочки "Статус персонала" и "Статус суперпользователя".


# Установка проекта

## Требования
Что бы установить проект лучше всего использовать Ubuntu 14.04 (или выше) в качестве ОС.

## Установка
**Что бы развернуть ещё одну копию проекта необходимо:**

0. Направить новый домен на сервер, либо использовать отдельный порт, который ещё не занят в настройках Nginx.

1. Авторизоваться на сервере по ssh командой ```ssh имя_пользователя@адрес_сервера```

2. **Если установка идёт на новый сервер** необходимо от имени пользователя root запустить сктипт ```vk_reposter/etc/install_external_requirements.sh```. 
Данный скрипт установит необходимое ПО для развёртывания сервера.

3. Получить права пользователя reposter командой ```sudo su reposter```. Следующие 2 пункта будут выполняться от имени этого пользователя.

4. Скопировать директорию **/home/reposter/vk_reposter/** в новое место размещение нового проекта, например ```cp ~/vk_reposter ~/vk_reposter2```

5. Запустить файл ```~/vk_reposter2/vk_reposter/etc/install.sh```. 
Данный скрипт произведёт очистку старой БД и произведёт инициализацию проекта.
Когда исполнение скрипта дойдёт до **CREATE ADMIN USER** необходимо будет ввести "имя пользователя", "email" и "пароль".
Этот логин и пароль будет использоваться для входа в [Админку](http://grigory.keeper.fvds.ru/).
Скрипт должен завершиться сообщением **INSTALLATION SUCCESSFULLY COMPLETED**.

6. Получить права пользователя root командой ```sudo su```, либо ```exit```, если ранее был совершён вход под рутом.

7. Создать новую конфигурацию Supervisor в директорию **/etc/supervisor/conf.d**, скопировав в неё файл **vk_reposter/etc/conf/supervisor.conf** из проекта.
Например это можно сделать командой ```cp ~/vk_reposter/vk_reposter/etc/conf/supervisor.conf /etc/supervisor/conf.d/reposter.conf```.
Затем нужно открыть созданный файл ```nano /etc/supervisor/conf.d/reposter.conf``` и заменить:
{{ПОРЯДКОВЫЙ_НОМЕР_ПРОЕКТА}} - должен быть уникальным; 
{{АБСОЛЮТНЫЙ_ПУТЬ_К_ДИРЕКТОРИИ_ПРОЕКТА}} - полный путь к директории, например /home/reposter/vk_reposter;
{{ПОРТ_НА_КОТОРОМ_ЗАПУЩЕН_GUNICORN}} - порт который ещё не занят, например 8001.
Заменить надо на реальные данные.

8.  Обновить конфигурацию supervisor ```sudo supervisorctl update```

9. Создать новую конфигурацию Nginx в директории **/etc/nginx/sites-enabled**, скопировав в неё файл **vk_reposter/etc/conf/nginx.conf** из проекта.
Например это можно сделать командой ```cp ~/vk_reposter/vk_reposter/etc/conf/nginx.conf /etc/nginx/sites-enabled/reposter.conf```.
Затем нужно открыть созданный файл ```nano /etc/nginx/sites-enabled/reposter.conf``` и заменить:
{{АДРЕС_СЕРВЕРА}} - должен быть уникальным; 
{{АБСОЛЮТНЫЙ_ПУТЬ_К_ДИРЕКТОРИИ_ПРОЕКТА}} - полный путь к директории, например /home/reposter/vk_reposter;
{{ПОРТ_НА_КОТОРОМ_ЗАПУЩЕН_GUNICORN}} - порт который ещё не занят, например 8001.
Заменить надо на реальные данные.

10. Обновить конфигурацию nginx ```sudo service nginx restart```

11. Зайти в админку по новому адресу (если на сервер было направлено новое имя) или порту.
Используем логин и пароль, который вводили в пункте 5.
Если всё нормально - переходим к самому началу инструкции "Подготовка Вконтакте".


# Управление сервером
Для запуска сервера используется [Supervisor](http://supervisord.org/).
При старте сервера демон супервизора автоматически запустит необходимые процессы.

```sudo supervisorctl status - отображает состояние процессов```

```sudo supervisorctl restart all - рестартует проект все проекты```
