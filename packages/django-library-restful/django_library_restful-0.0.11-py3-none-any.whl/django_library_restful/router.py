from rest_framework.routers import DefaultRouter
from .views import *

bookstore_api_router = DefaultRouter()

bookstore_api_router.register('user', UserViewSet)
bookstore_api_router.register('book', BookViewSet)
bookstore_api_router.register('library', LibraryViewSet)
bookstore_api_router.register('shelf', ShelfViewSet)
bookstore_api_router.register('detail/shelf', ShelfDetailViewSet)
bookstore_api_router.register('detail/library', LibraryDetailViewSet)
bookstore_api_router.register('borrow', BorrowViewSet)