from rest_framework import pagination


class LmsPaginator(pagination.PageNumberPagination):
    """
    Пагинатор для вывода всех уроков и курсов.
    """
    page_size = 3
    page_query_param = 'page_size'
    max_page_size = 30
