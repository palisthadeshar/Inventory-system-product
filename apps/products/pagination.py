from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination
from rest_framework.response import Response


# class Pagination(LimitOffsetPagination):
#     default_limit = 3
#     limit_query_param = 'l' 
#     offset_query_param = 'o'
#     max_limit = 1

class Pagination(PageNumberPagination):
    page_size=2
    limit=2

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
    
 
    


