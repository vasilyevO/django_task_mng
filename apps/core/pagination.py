from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    """Постраничная навигация: 5 объектов на страницу."""

    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50