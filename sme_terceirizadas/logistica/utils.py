from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class RequisicaoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data, num_enviadas):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('num_enviadas', num_enviadas),
            ('results', data)
        ]))