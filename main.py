import csv
import pathlib
from argparse import ArgumentParser, Namespace
import re
from pathlib import Path
from typing import List, Any

from pydantic import ValidationError
from prettytable import from_csv, PrettyTable

from pagination import Pagination
from validator import PhonebookData

FIELDNAMES = ('id', 'last_name', 'first_name', 'middle_name', 'organization', 'work_phone', 'personal_phone')
CSV_FILE = Path().resolve().joinpath('phonebook.csv') # настроить проверку csv


class CSVPhonebook:

    def __init__(self, file: pathlib.PosixPath = CSV_FILE):
        self.file = file
        self.encoding = 'utf-8'

    @property
    def get_all(self) -> list[list]:
        """
        Возвращает все элементы таблицы
        TODO объяснить почему именно  DictReader
        """
        with open(file=self.file, mode='r', newline='', encoding=self.encoding) as csvfile:
            reader: csv.DictReader = csv.DictReader(csvfile)
            return [list(row.values()) for row in reader]

    @property
    def get_last_id(self) -> int:
        """
        Достаёт последний id из таблицы. Необходим для операции -с/--create.
        """
        return int(self.get_all[-1][0])

    def create(self, data: PhonebookData):
        with open(file=self.file, mode='a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            writer.writerow(data.model_dump())

    def get_one(self, id: int) -> str:
        """Возвращает запись по ключу id"""
        index = id - 1
        try:
            return self.get_all[index]
        except IndexError:
            pass

    def delete(self, id: int):
        """Удаление записей по id"""
        rows = [x for x in self.get_all if x[0] != str(id)]
        try:
            if id == -1:
                del rows[-1]
        except IndexError:
            rows =[]

        with open(file=self.file, mode='w', newline='', encoding=self.encoding) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(FIELDNAMES)
            writer.writerows(rows)

    def search(self, phrase: str):
        """TODO ПОЛНОСТЬЮ ПЕРЕРОБАТЫВАТЬ В СООТВЕСТВИИ С ТРЕБОВАНИМИ"""
        search_fieldname = ''
        if phrase.isdigit():
            search_fieldname = 'personal_phone'
        if phrase.isalpha():
            phrase = phrase.title()
            search_fieldname = 'last_name'
        with open(file=self.file, mode='r', newline='', encoding=self.encoding) as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=FIELDNAMES)
            result = [row for row in reader if phrase in row[search_fieldname]]
        return result


parser = ArgumentParser(
    prog='Phonebook CLI',
    description='Программа CRUD для записей в телефонном справочнике',
    epilog='Text at the bottom of help'
)

pt = PrettyTable()
pt.field_names = FIELDNAMES
phonebook = CSVPhonebook(CSV_FILE)


def pagination(per_page: int = 5, page: int = 0):
    page_index = page - 1
    ph = Pagination(collection=phonebook.get_all, items_per_page=per_page)
    try:
        for row in ph.total[page_index]:
            pt.add_row(row)

        print(f"Page number {page} of {ph.page_count()} pages")
        return pt
    except IndexError:
        return f"Out of range. Only {ph.page_count()} pages in the phone book"


if __name__ == '__main__':
    parser.add_argument('-c', '--create', help='Create entry', action='append', nargs=3)
    parser.add_argument('-u', '--update', help='Update entry', action='store', type=int)
    parser.add_argument('-d', '--delete', help='Delete entry', action='store', type=int)
    parser.add_argument('-s', '--search', help='Search entry', action='store', nargs='*')
    parser.add_argument('-p', '--page', help='', action='store', type=int)

    args: Namespace = parser.parse_args()

    if args.create:
        try:
            data = PhonebookData(
                id=phonebook.get_last_id + 1,
                last_name=args.create[0][0],
                first_name=args.create[0][1],
                personal_phone=args.create[0][2]
            )
        except ValueError:
            raise "bad data"

        phonebook.create(data=data)
        pt.add_row(phonebook.get_one(data.id))
        print(pt)

    elif args.update:
        input("введи имя: ")

    elif args.search:
        print(phonebook.search(phrase=args.search[0]))

    elif args.delete:
        phonebook.delete(args.delete)

    elif args.page:
        print(pagination(page=args.page))
    else:
        print(pagination(page=1))
