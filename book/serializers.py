from rest_framework.serializers import ModelSerializer, SerializerMethodField, IntegerField, DecimalField

from book.models import Book, UserBookRelation


class BooksSerializer(ModelSerializer):
    annotated_likes = IntegerField(read_only=True)
    rating = DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'author', 'annotated_likes', 'rating']


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ['book', 'like', 'in_bookmarks', 'rate']