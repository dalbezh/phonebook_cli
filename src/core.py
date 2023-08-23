from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import List, Union

from pydantic_extra_types.phone_numbers import PhoneNumber

from .validator import CreateField, PhoneField

FIELDNAMES = ('id', 'last_name', 'first_name', 'middle_name', 'organization', 'work_phone', 'personal_phone')


class CSVPhonebook:
    """Отвечает за работу с файлом справочника"""
    def __init__(self, file: Path):
        self.file = file
        self.encoding = 'utf-8'

    @property
    def get_all(self) -> list[list]:
        """
        Возвращает все элементы таблицы
        DictReader выбран с тем условием, что он читает имена колонок и не сохраняет их в результат.
        """
        with open(file=self.file, mode='r', newline='', encoding=self.encoding) as csvfile:
            reader: csv.DictReader = csv.DictReader(csvfile)
            return [list(row.values()) for row in reader]

    @property
    def get_last_id(self) -> int:
        """Достаёт последний id из таблицы. Необходим для операции с ключом -c/--create."""
        try:
            return int(self.get_all[-1][0])
        except IndexError:
            return 0

    def get_one(self, id: int) -> list:
        """Возвращает запись по ключу id"""
        try:
            index = id - 1
            result = self.get_all[index]
        except IndexError:
            pass
        return result

    def create(self, data: CreateField):
        """Добавляет новую созданную запись в конец файла"""
        with open(file=self.file, mode='a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            writer.writerow(data.model_dump())

    def update(self, id: int, fieldname: str, data: str = '') -> List[list]:
        """Обновление данных"""
        result = []
        for row in self.get_all:
            if row[0] == str(id) and fieldname in FIELDNAMES and data != '':
                row[FIELDNAMES.index(fieldname)] = data
            result.append(row)
        return result

    def delete(self, id: int) -> List[list]:
        """
        Удаление записей по id
        Реализована проверка в случаи удаления последней записи
        """
        result = [row for row in self.get_all if row[0] != str(id)]
        try:
            if id == -1:
                del result[-1]
        except IndexError:
            result = []
        return result

    def overwrite(self, rows: List[list]):
        """Нужен для self.update и self.delete"""
        with open(file=self.file, mode='w', newline='', encoding=self.encoding) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(FIELDNAMES)
            writer.writerows(rows)

    def search(self, search_phrase: Union[str, PhoneNumber]) -> List[list]:
        """Поиск по справочнику"""
        result = []
        if search_phrase.startswith('+'):
            try:
                phone = PhoneField(phone=search_phrase)
                for row in self.get_all:
                    if phone.phone in row:
                        result.append(row)
            except ValueError:
                pass
        if search_phrase.isalpha():
            for row in self.get_all:
                if re.search(search_phrase, row[1], flags=re.IGNORECASE):
                    result.append(row)
                elif re.search(search_phrase, row[2], flags=re.IGNORECASE):
                    result.append(row)
                elif re.search(search_phrase, row[3], flags=re.IGNORECASE):
                    result.append(row)
                elif re.search(search_phrase, row[4], flags=re.IGNORECASE):
                    result.append(row)
        return result
