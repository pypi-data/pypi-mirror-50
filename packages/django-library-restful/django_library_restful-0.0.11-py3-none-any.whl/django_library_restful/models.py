from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Book(models.Model):
    name = models.CharField('name', max_length=50)
    author = models.CharField('author', max_length=50)
    user = models.ManyToManyField(User, through='Borrow', related_name='books', null=True, verbose_name='user')

    def __str__(self):
        return self.name


class Library(models.Model):
    name = models.CharField('name', max_length=50)
    address = models.CharField('address', max_length=50)
    city = models.CharField('city', max_length=20, default='تهران')
    books = models.ManyToManyField(Book, through='LibraryDetail', related_name='libraries', verbose_name='books')

    def __str__(self):
        return self.name


class Shelf(models.Model):
    books = models.ManyToManyField(Book, through='ShelfDetail', verbose_name='books')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='shelves', verbose_name='library')
    number = models.IntegerField('number')

    def __str__(self):
        return 'shelf ' + str(self.number)

    def library_name(self):
        return self.library.name


class ShelfDetail(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='book', related_name='shelf_details')
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, verbose_name='book shelf', related_name='shelf_details')
    number = models.IntegerField('count', default=1)

    def save(self, *args, **kwargs):
        """if book exist in shelf , number of this is increased else is created"""
        try:
            detail = ShelfDetail.objects.get(shelf=self.shelf, book=self.book)
            detail.number += self.number
            detail.update(*args, **kwargs)
        except ShelfDetail.DoesNotExist:
            super(ShelfDetail, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        """if book exist in shelf , number of this is increased else is created"""
        super(ShelfDetail, self).save(*args, **kwargs)

    def library_name(self):
        return self.shelf.library_name()

    def borrow(self):
        self.number -= 1
        return self.number

    def back(self):
        self.number += 1
        return self.number

    def __str__(self):
        return self.shelf.__str__() + ', ' + self.book.__str__()


class LibraryDetail(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='book', related_name='library_details')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, verbose_name='library',
                                related_name='library_details')

    def save(self, *args, **kwargs):
        try:
            detail = LibraryDetail.objects.get(book=self.book, library=self.library)
        except LibraryDetail.DoesNotExist:
            super(LibraryDetail, self).save(*args, **kwargs)

    def library_name(self):
        return self.library.name


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', related_name='borrows')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='book', related_name='borrows')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, verbose_name='library', null=True,
                                related_name='borrows')
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, verbose_name='shelf', null=True, related_name='borrows')
    get_date = models.DateField('borrow date', auto_now_add=True)
    return_date = models.DateField('return date', null=True, blank=True)

    def user_name(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if self.return_date:
            "if book that borrowed is back, increase the number of book"
            self.back()
        else:
            "else decrease the number of book"
            self.borrow()
        super(Borrow, self).save(*args, **kwargs)

    def borrow(self):
        detail = ShelfDetail.objects.get(book=self.book, shelf=self.shelf)
        detail.borrow()
        detail.update()
        pass

    def back(self):
        detail = ShelfDetail.objects.get(book=self.book, shelf=self.shelf)
        detail.back()
        detail.update()
        pass
