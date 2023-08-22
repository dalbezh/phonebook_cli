from typing import List


class Pagination:
    """
    Предназначен для пагинации полученных данных
    """

    def __init__(self, collection: list, items_per_page: int):
        self.collection = collection
        self.items_per_page = items_per_page

    @property
    def total(self) -> List[dict]:
        """
        TODO дописать DOC. Мб переписать в лонг.
        также стоит переписать чутка (значение временных переменных переменных)
        """
        return [
            self.collection[i:i + self.items_per_page]
            for i in range(0, len(self.collection), self.items_per_page)
        ]

    def page_count(self) -> int:
        """Возвращает количество получившихся страниц"""
        return len(self.total)

    def page_index(self) -> int:
        """
        TODO подумать и переработать
        """
        return 0
