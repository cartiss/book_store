from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK

from book.models import Book
from book.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(name='Test book 1', price=100)
        self.book2 = Book.objects.create(name='Test book 2', price=150)

    def test_get(self):
        url = reverse('book-list')
        resp = self.client.get(url)
        serializer_data = BooksSerializer([self.book1, self.book2], many=True).data

        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(HTTP_200_OK, resp.status_code)


