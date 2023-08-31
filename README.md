Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

Стек
- python
- flask
- sqlite

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* сли у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запуск проекта
```
flask run
```

У проекта есть API
- api/id/ - POST запрос на создание новой короткой ссылки
- api/id/<short_id>/ - GET запрос на получение оригинальной ссылки по указанному короткому идентификатору

Примеры запросов 
1.
{
  "url": "string",
  "custom_id": "string"
}
2.api/id/short_link 
Пример ответа

{
  "url": "string"
}