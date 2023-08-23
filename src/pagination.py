from typing import List


class Pagination:
    """
    Предназначен для пагинации справочника
    """

    def __init__(self, collection: List[list], items_per_page: int):
        self.collection = collection
        self.items_per_page = items_per_page

    @property
    def total(self) -> List[List[list]]:
        """
        Возвращает вложенный список списков
        """
        result = []
        for index in range(0, len(self.collection), self.items_per_page):
            result += [self.collection[index:index + self.items_per_page]]
        return result

    @property
    def page_count(self) -> int:
        """Возвращает количество получившихся страниц"""
        return len(self.total)
