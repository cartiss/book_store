from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK

from book.models import Book
from book.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(name='Test book 1', price=100, author='Author 1')
        self.book2 = Book.objects.create(name='Test book 2', price=150, author='Author 1')
        self.book3 = Book.objects.create(name='Test book Author 1', price=200, author='Author 2')

    def test_get(self):
        url = reverse('book-list')
        resp = self.client.get(url)
        serializer_data = BooksSerializer([self.book1, self.book2, self.book3], many=True).data

        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(HTTP_200_OK, resp.status_code)


    def test_filter(self):
        url = reverse('book-list')
        resp = self.client.get(url, data={'price': 100})
        serializer_data = BooksSerializer([self.book1], many=True).data

        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(HTTP_200_OK, resp.status_code)

    def test_filter_negative(self):
        url = reverse('book-list')
        resp = self.client.get(url, data={'price': 99999999})
        serializer_data = BooksSerializer(many=True).data

        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(HTTP_200_OK, resp.status_code)

    def test_search(self):
        url = reverse('book-list')
        resp = self.client.get(url, data={'search': 'Author'})
        serializer_data = BooksSerializer([self.book1, self.book2, self.book3], many=True).data

        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(HTTP_200_OK, resp.status_code)

    def test_search_negative(self):
        url = reverse('book-list')
        resp = self.client.get(url, data={'search': 'Negative'})
        serializer_data = BooksSerializer(many=True).data

        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(HTTP_200_OK, resp.status_code)

    def test_ordering(self):
        url = reverse('book-list')
        resp = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BooksSerializer([self.book1, self.book2, self.book3], many=True).data

        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(HTTP_200_OK, resp.status_code)

    def test_ordering_negative(self):
        url = reverse('book-list')
        resp = self.client.get(url, data={'ordering': '-price'})
        serializer_data = BooksSerializer([self.book3, self.book2, self.book1], many=True).data

        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(HTTP_200_OK, resp.status_code)
