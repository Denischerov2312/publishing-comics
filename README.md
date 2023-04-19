# Публикация комиксов

Скрипт публикует случайный комикс на стене в Вконтакте.

### Как установить
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

Рядом с самим скриптом надо создать файл `.env` и вписать туда `CLIENT_ID`, `ACCESS_TOKEN` и `GROUP_ID`
Пример:
```
VK_CLIENT_ID=97e702019727020597e70201a054f5c4308997e797e70201f41216935340f9cc7d49e89c
VK_ACCESS_TOKEN=vk1.a.JeTp8WHEf1RkmZwroJWNXrNgLSuTPEkKZcV8jbeOjudTVQ9Tx2KkdxD4ZsMEjHAz9lBR13Xjy-THLr-
VK_GROUP_ID=514953997
```

Скрипт не имеет аргументов, пример запуска:
```
> python publish_random_comic.py
{'response': {'post_id': 8}}
```
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
