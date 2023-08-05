from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(many=True, view_name='book-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'books']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    libraries = serializers.HyperlinkedRelatedField(many=True, view_name='library-detail', read_only=True)
    shelf_details = serializers.HyperlinkedRelatedField(many=True, view_name='shelfdetail-detail', read_only=True)
    borrows = serializers.HyperlinkedRelatedField(many=True, view_name='borrow-detail', read_only=True)

    class Meta:
        model = Book
        fields = ['name', 'author', 'user', 'libraries', 'borrows', 'shelf_details']


class LibrarySerializer(serializers.HyperlinkedModelSerializer):
    shelves = serializers.HyperlinkedRelatedField(many=True, view_name='shelf-detail', read_only=True)
    library_details = serializers.HyperlinkedRelatedField(many=True, view_name='librarydetail-detail', read_only=True)
    borrows = serializers.HyperlinkedRelatedField(many=True, view_name='borrow-detail', read_only=True)

    class Meta:
        model = Library
        fields = ['name', 'address', 'city', 'books', 'shelfs', 'library_details', 'borrows']


class ShelfSerializer(serializers.HyperlinkedModelSerializer):
    shelf_details = serializers.HyperlinkedRelatedField(many=True, view_name='shelfdetail-detail', read_only=True)
    borrows = serializers.HyperlinkedRelatedField(many=True, view_name='borrow-detail', read_only=True)

    class Meta:
        model = Shelf
        fields = ['library', 'number', 'books', 'shelf_details', 'borrows']


class ShelfDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShelfDetail
        fields = '__all__'


class LibraryDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LibraryDetail
        fields = '__all__'


class BorrowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Borrow
        fields = '__all__'
