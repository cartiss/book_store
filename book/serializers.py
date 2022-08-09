from rest_framework.serializers import ModelSerializer

from book.models import Book


class BooksSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'author']