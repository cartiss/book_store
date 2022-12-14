from django.db.models import Count, Case, When, Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from book.models import Book, UserBookRelation
from book.permissions import IsOwnerOrStaffOrReadOnly
from book.serializers import BooksSerializer, UserBookRelationSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).select_related('owner')
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ['price', ]
    search_fields = ['name', 'author']
    ordering_fields = ['price', 'name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        super().perform_create(serializer)


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        return obj


def auth(request):
    return render(request, 'oauth.html')
