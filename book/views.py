from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from book.models import Book
from book.serializers import BooksSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('price', )
    search_fields = ('name', 'author')
