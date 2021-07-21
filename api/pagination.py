from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 5
    # page_query_param = "p"
    # page_size_query_param = "product"
    # max_page_size = 6
