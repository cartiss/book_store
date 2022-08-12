from rest_framework.serializers import ModelSerializer

from book.models import Book, UserBookRelation


class BooksSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'author']


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ['book', 'like', 'in_bookmarks', 'rate']