from django.contrib.auth.models import User
from django.test import TestCase

from book.logic import set_rating
from book.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user1')
        self.user2 = User.objects.create(username='test_user2')
        self.user3 = User.objects.create(username='test_user3')
        self.book1 = Book.objects.create(name='Test book 1', price=100, author='Author', owner=self.user1)

        UserBookRelation.objects.create(user=self.user1, book=self.book1, like=True, rate=2)
        UserBookRelation.objects.create(user=self.user2, book=self.book1, like=True, rate=3)
        UserBookRelation.objects.create(user=self.user3, book=self.book1, like=True, rate=1)

    def test_ok(self):
        set_rating(self.book1)
        self.book1.refresh_from_db()
        self.assertEqual('2.00', str(self.book1.rating))