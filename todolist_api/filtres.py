from django.db.models import QuerySet
from typing import List, Optional


def filter_by_status(queryset: QuerySet, status_code: Optional[List]) -> QuerySet:
    """
    Фильтрация по статусу записи
    :param queryset: исходный queryset
    :param status_code: список состояний
    :return: модернизированный queryset
    """
    if status_code is None:
        return queryset
    queryset = queryset.filter(status__in=status_code)
    return queryset


def filter_by_important(queryset: QuerySet, important: Optional[bool]):
    """
    Фильтрация по полю "Важность"
    :param queryset: исходный queryset
    :param important: Bool True / False
    :return: модернизированный queryset
    """
    if important is None:
        return queryset
    queryset = queryset.filter(important=important)
    return queryset


def filter_by_public(queryset: QuerySet, public: Optional[bool]):
    """
    Фильтрация по полю "Публичность"
    :param queryset: исходный queryset
    :param public: Bool True / False
    :return: модернизированный queryset
    """
    if public is None:
        return queryset
    queryset = queryset.filter(public=public)
    return queryset

