from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permisions import IsSuperUserOrReadOnly
from .serializer import *

permissions = [IsAuthenticatedOrReadOnly, IsSuperUserOrReadOnly]


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = permissions


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = permissions


class LibraryViewSet(ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = permissions


class ShelfViewSet(ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    permission_classes = permissions


class ShelfDetailViewSet(ModelViewSet):
    queryset = ShelfDetail.objects.all()
    serializer_class = ShelfDetailSerializer
    permission_classes = permissions


class LibraryDetailViewSet(ModelViewSet):
    queryset = LibraryDetail.objects.all()
    serializer_class = LibraryDetailSerializer
    permission_classes = permissions


class BorrowViewSet(ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = permissions
