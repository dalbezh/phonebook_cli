# <p align="center">PHONEBOOK CLI</p>

![Python](https://img.shields.io/badge/python-3.9-blue?logo=python&logoColor=FFE873)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Краткое описание
Программа с интерфейсом командной строки для создания, чтения, обновления и удаления записей в телефонном справочнике.

## Функционал
Для того чтобы ознакомится с функционалом интерфейса командной строки необходимо ввести:
```commandline
$ python3 main.py --help
```
```commandline
usage: Phonebook CLI [-h] [-c CREATE CREATE CREATE] [-u UPDATE] [-d DELETE] [-s SEARCH] [-p PAGE]

Программа CRUD для записей в телефонном справочнике

optional arguments:
  -h, --help            show this help message and exit
  -c CREATE CREATE CREATE, --create CREATE CREATE CREATE
                        Create entry
  -u UPDATE, --update UPDATE
                        Update entry
  -d DELETE, --delete DELETE
                        Delete entry
  -s SEARCH, --search SEARCH
                        Search entry
  -p PAGE, --page PAGE  Pagination method
```
### Вывод данных (`-p / --page` или без ключей)
Для вывода таблицы в консоль можно воспользоваться следующими командами:
```commandline
вывести первую страницу:
$ python3 main.py 

Вывести N-ую страницу:
$ python3 main.py -p 2
```
Пагинация при выводе таблицы установленна по умолчанию.

### Создание (`-с / --create`)
Для создания записи нужно передать 3 обязательных поля: Фамилия, Имя и номер личного телефона:
```commandline
$ python3 main.py -c Иванов Иван +79996665515
```
Телефон должен начинаться на `+` и после иметь 11 цифр.
При создании есть проверка на дублированный номер. В случаи ее срабатывания программа отдаст сообщение с номером id
в которой найден дубль: `A row with this phone number already exists: id N`.

### Обновление (`-u / --update`)
При работе с обновлением нужно знать номер id записи в которой необходимо изменить номер:
```commandline
$ python3 main.py -u 1
```
Если запись с таким id есть, будет предложен список полей который можно изменить:
```commandline
1 last_name
2 first_name
3 middle_name
4 organization
5 work_phone
6 personal_phone
Input a number from 1 to 6 for the field you want to change:
```
После выбора нужно ввести новое значение поля, и в конце программа отдаст обновленную запись.

### Удаление (`-d / --delete`)
Удаление происходит по id
```commandline
$ python3 main.py -d 3
```
В консоль ничего не выводится, запись либо удаляется при нахождении id, либо таблица остаётся без изменений.

### Поиск (`-s / --search`)
Поиск реализован по всем полям кроме id. С поиском по полям номеров телефонов работает только полное совпадение,
то есть для поиска нужно ввести номер целиком в формате `+79991112233` или `+7495-777-12-12`. С остальными полями поиск
работает как по части слова так и целиком (регистр не важен).
```commandline
$ python3 main.py -s +79231111121
```
Вывод найденной записи:
```commandline
+----+-----------+------------+-------------+--------------+----------------------+----------------------+
| id | last_name | first_name | middle_name | organization |      work_phone      |    personal_phone    |
+----+-----------+------------+-------------+--------------+----------------------+----------------------+
| 4  |   Конор   |    Сара    |             |  OOO SkyNet  | tel:+1-123-111-11-21 | tel:+7-923-111-11-21 |
+----+-----------+------------+-------------+--------------+----------------------+----------------------+
```
Поиск по фразе:
```commandline
$ python main.py -s ива
```
Вывод найденных записи:
```commandline
+----+-----------+------------+-------------+--------------+----------------------+----------------------+
| id | last_name | first_name | middle_name | organization |      work_phone      |    personal_phone    |
+----+-----------+------------+-------------+--------------+----------------------+----------------------+
| 2  |   Иванов  |    Иван    |             |              |                      | tel:+7-999-666-55-44 |
| 5  |   Гусев   |    Петр    |   Иванович  |              | tel:+7-499-888-12-12 | tel:+7-967-888-12-01 |
+----+-----------+------------+-------------+--------------+----------------------+----------------------+
```

## Структура приложения
В [main.py](./main.py) находятся основные вызовы в блоке `__name__ == '__main__'`. В main.py создаются все необходимые объекты, 
а также имеется три функции которые отвечают за отображении, поиск и создание данных. Их предназначение вспомогательный,
и вынесено отдельно чтобы не перегружать основную логику работы со справочником.\
_Файл справочник [phonebook.csv](./phonebook.csv) должен находится в той же директории, что и main.py_\
\
Вспомогательные объекты и основной класс работы со справочником расположены в [./src](./src).\
В core.py расписан CSVPhonebook со всеми необходимыми методами и свойствами для работы с файлом. 
Для пагинации в pagination.py есть Pagination, у него всего два свойства для получения многомерного списка и его длины.
Для корректной записи и поиска телефонных номеров в validator.py есть валидатора.

## Зависимости
Для отображения таблиц используются `prettytable==3.8.0`\
Для валидацию данных при создании и редактировании был взят `pydantic==2.2.1`, также для работы с полями номеров 
телефонов необходима `pydantic-extra-types==2.0.0` в которой есть объект PhoneNumber.\
Зависимости для работы самого приложения находятся в файле [requirements.txt](./requirements.txt).\
Для прогона линтера и статической проверки типов есть файл [requirements_tests.txt](./requirements_tests.txt).


___
## Выполенные критерии:
1. Вывод постранично записей из справочника на экран
2. Добавление новой записи в справочник
3. Возможность редактирования записей в справочнике
4. Поиск записей по одной или нескольким характеристикам
5. Интерфейс реализован через консоль.
6. Данных хранятся организовано в виде текстового файла в формате [csv](./phonebook.csv)
7. В справочнике хранится следующая информация: фамилия, имя, отчество, название организации, телефон рабочий, телефон личный (сотовый)
#### +
8. Функции и переменные аннотированы
9. Функции и методы документированы
10. Описана документация программы
___
## TODO

* Из минусов алгоритма работы программы: при изменении или удалении элемента забирается в память и перезаписывается весь файл, следовательно, огромные файлы данное приложением на данном этапе лучше не грузить. 
Для этого предусмотрена проверка при инициализации файла phonebook.csv.
* На данный момент поля номеров телефонов не обновляются.