# disk_explorer
Программа для анализа содержания каталога

## Предварительная установка

Создание виртуальной среды:

```commandline
python -m venv .venv
.\.venv\Scripts\activate
```

Установка библиотек:

```commandline
pip install PySide6
```

## Сборка проекта
Сборка файла ресурсов:

```commandline
python .\.venv\Scripts\pyside6-rcc.exe .\resources\resources.qrc -o .\resources\resources_rc.py
```

Сборка файла с дизайном приложения:

```commandline
python .\.venv\Scripts\pyside6-uic.exe .\ui\main_window.ui -o .\ui\compiled_ui.py --absolute-imports
```
