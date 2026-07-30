from rest_framework.pagination import PageNumberPagination


class ProductsPagination(PageNumberPagination):
    page_size = 14
    page_size_query_param = "page_size"
    max_page_size = 28  # limite máximo de intens por pagina