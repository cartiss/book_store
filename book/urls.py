from django.urls import path, include
from rest_framework.routers import SimpleRouter

from book.views import BookViewSet, auth, UserBookRelationView

router = SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBookRelationView)

urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    path('auth/', auth, name='git_auth'),
]

urlpatterns += router.urls
