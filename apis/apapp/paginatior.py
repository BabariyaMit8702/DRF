from rest_framework.pagination import CursorPagination

class mycursor(CursorPagination):
    page_size = 3
    ordering = 'name'