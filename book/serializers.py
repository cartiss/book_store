from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField, IntegerField, DecimalField, CharField

from book.models import Book, UserBookRelation


class BooksSerializer(ModelSerializer):
    annotated_likes = IntegerField(read_only=True)
    owner_name = CharField(source='owner.username', default="", read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'author', 'annotated_likes', 'rating', 'owner_name']


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ['book', 'like', 'in_bookmarks', 'rate']