import json

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, \
    HTTP_400_BAD_REQUEST

from book.models import Book, UserBookRelation
from book.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user1')
        self.user2 = User.objects.create(username='test_user2')
        self.book1 = Book.objects.create(name='Test book 1', price=100, author='Author 1', owner=self.user2)
        self.book2 = Book.objects.create(name='Test book 2', price=150, author='test 1')
        self.book3 = Book.objects.create(name='Test book Author 1', price=200, author='Author 2')

        UserBookRelation.objects.create(user=self.user1, book=self.book1, like=True, rate=2)

    def test_get(self):
        url = reverse('book-list')
        resp = self.client.get(url)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data

        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(HTTP_200_OK, resp.status_code)
        self.assertEqual(serializer_data[0]['rating'], '2.00')
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)

    def test_filter(self):
        url = reverse('book-list')
        resp = self.client.get(url, data={'price': 100})
        books = Book.objects.filter(id__in=[self.book1.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))))
        serializer_data = BooksSerializer(books, many=True).data

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
        books = Book.objects.filter(id__in=[self.book1.id, self.book3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data
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
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('price')
        serializer_data = BooksSerializer(books, many=True).data

        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(HTTP_200_OK, resp.status_code)

    def test_ordering_negative(self):
        url = reverse('book-list')
        resp = self.client.get(url, data={'ordering': '-price'})
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('-price')
        serializer_data = BooksSerializer(books, many=True).data

        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(HTTP_200_OK, resp.status_code)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            'name': 'Test book create',
            'price': 100,
            'author': 'Author 1',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        resp = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(HTTP_201_CREATED, resp.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user1, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            'name': self.book1.name,
            'price': 500,
            'author': self.book1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        resp = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(HTTP_200_OK, resp.status_code)

        self.book1.refresh_from_db()
        self.assertEqual(data['price'], self.book1.price)

    def test_update_not_owner(self):
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            'name': self.book1.name,
            'price': 500,
            'author': self.book1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        resp = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(HTTP_403_FORBIDDEN, resp.status_code)
        initial_price = self.book1.price
        self.book1.refresh_from_db()
        self.assertEqual(initial_price, self.book1.price)

    def test_update_not_owner_but_stuff(self):
        self.user_admin = User.objects.create(username='test_admin', is_staff=True)
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            'name': self.book1.name,
            'price': 600,
            'author': self.book1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)
        resp = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(HTTP_200_OK, resp.status_code)
        initial_price = self.book1.price
        self.book1.refresh_from_db()
        self.assertEqual(data['price'], self.book1.price)

    def test_patch_update(self):
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            'price': 500,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        resp = self.client.patch(url, data=json_data, content_type='application/json')

        self.assertEqual(HTTP_200_OK, resp.status_code)

        self.book1.refresh_from_db()
        self.assertEqual(data['price'], self.book1.price)

    def test_delete(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book1.id,))
        self.client.force_login(self.user2)
        resp = self.client.delete(url)

        self.assertEqual(HTTP_204_NO_CONTENT, resp.status_code)
        self.assertEqual(2, Book.objects.all().count())

    def test_delete_no_login(self):
        url = reverse('book-detail', args=(self.book1.id,))
        resp = self.client.delete(url)

        self.assertEqual(HTTP_403_FORBIDDEN, resp.status_code)
        self.assertEqual(3, Book.objects.all().count())


class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user1')
        self.user2 = User.objects.create(username='test_user2')
        self.book1 = Book.objects.create(name='Test book 1', price=100, author='Author 1', owner=self.user2)
        self.book2 = Book.objects.create(name='Test book 2', price=150, author='Author 1')

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        resp = self.client.patch(url, data=json_data, content_type='application/json')
        self.book1.refresh_from_db()
        self.assertEqual(HTTP_200_OK, resp.status_code)
        relation = UserBookRelation.objects.get(user=self.user2,
                                                book=self.book1)
        self.assertTrue(relation.like)

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            "rate": 2,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        resp = self.client.patch(url, data=json_data, content_type='application/json')
        self.book1.refresh_from_db()
        self.assertEqual(HTTP_200_OK, resp.status_code)
        relation = UserBookRelation.objects.get(user=self.user2,
                                                book=self.book1)
        self.assertEqual(data['rate'], relation.rate)

    def test_rate_wrong(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            "rate": 11,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        resp = self.client.patch(url, data=json_data, content_type='application/json')
        self.book1.refresh_from_db()
        self.assertEqual(HTTP_400_BAD_REQUEST, resp.status_code)
