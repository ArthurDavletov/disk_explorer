# disk_explorer
Программа для анализа содержания каталога

## Предварительная установка

Создание виртуальной среды:

```powershell
python -m venv .venv
```

Включение виртуальной среды:

```powershell
.\.venv\Scripts\activate
```

Установка библиотек:

```powershell
pip install -r requirements.txt
```

## Сборка проекта (Windows)

Сборка файла ресурсов:

```powershell
python .\.venv\Scripts\pyside6-rcc.exe .\resources\resources.qrc -o .\resources\resources_rc.py
```

Сборка файла с дизайном приложения:

```powershell
python .\.venv\Scripts\pyside6-uic.exe .\ui\main_window.ui -o .\ui\compiled_ui.py --absolute-imports
```

## Сборка (Linux)

Сборка файла ресурсов:

```commandline
pyside6-rcc ./resources/resources.qrc -o ./resources/resources_rc.py
```

```commandline
pyside6-uic ./ui/main_window.ui -o ./ui/compiled_ui.py --absolute-imports
```

## Сборка в бинарник

Для сборки дополнительно понадобится `pyinstaller`

```commandline
pip install pyinstaller
```

Windows:
```commandline
pyinstaller.exe -F main.py --noconsole
```

Linux:
```commandline
pyinstaller -F main.py --noconsole
```

Запускаемый файл будет находиться в `./dist/`