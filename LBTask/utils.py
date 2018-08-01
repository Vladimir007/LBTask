from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param


class FullPagePagintaion(PageNumberPagination):
    def get_paginated_response(self, data):
        url = self.request.build_absolute_uri()
        num_pages = self.page.paginator.num_pages

        return Response({
            'links': {
                'first': replace_query_param(url, self.page_query_param, 1) if self.page.number != 1 else None,
                'previous': self.get_previous_link(),
                'next': self.get_next_link(),
                'last': replace_query_param(url, self.page_query_param, num_pages)
                if self.page.number != num_pages else None
            },
            'per_page': self.page.paginator.per_page,
            'page': self.page.number,
            'num_pages': num_pages,
            'count': self.page.paginator.count,
            'results': data
        })
