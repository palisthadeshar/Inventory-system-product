from rest_framework import pagination

class MyPagination(pagination.LimitOffsetPagination):
    default_limit = 2
    limit_query_param = "l"
    offset_query_param = "o"
    max_limit = 4