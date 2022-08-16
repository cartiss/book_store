from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg, Sum, F, FloatField
from django.test import TestCase

from book.models import Book, UserBookRelation
from book.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user1')
        self.user2 = User.objects.create(username='test_user2')
        self.user3 = User.objects.create(username='test_user3')
        self.book1 = Book.objects.create(name='Test book 1', price=100, author='Author')
        self.book2 = Book.objects.create(name='Test book 2', price=150, author='Author2')

    def test_ok(self):
        UserBookRelation.objects.create(user=self.user1, book=self.book1, like=True, rate=2)
        UserBookRelation.objects.create(user=self.user2, book=self.book1, like=True, rate=3)
        UserBookRelation.objects.create(user=self.user3, book=self.book1, like=True, rate=1)

        UserBookRelation.objects.create(user=self.user1, book=self.book2, like=True, rate=0)
        UserBookRelation.objects.create(user=self.user2, book=self.book2, like=True, rate=6)
        UserBookRelation.objects.create(user=self.user3, book=self.book2, like=False, rate=2)

        books = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                            rating=Avg('userbookrelation__rate')),

        data = BooksSerializer(books, many=True).data
        print(data)
        expected_data = [
            {
                'id': self.book1.id,
                'name': 'Test book 1',
                'price': 100,
                'author': 'Author',
                'annotated_likes': 3,
                'rating': '2.00',
            },
            {
                'id': self.book2.id,
                'name': 'Test book 2',
                'price': 150,
                'author': 'Author2',
                'annotated_likes': 2,
                'rating': '2.67'
            },
        ]
        print(data)
        self.assertEqual(expected_data, data)
