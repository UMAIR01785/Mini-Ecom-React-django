from rest_framework.pagination import PageNumberPagination



class ProductPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 100
    page_query_param = 'page' 
    