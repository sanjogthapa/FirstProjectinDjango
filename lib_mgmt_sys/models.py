from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=123)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Books(models.Model):
    name = models.CharField(max_length=30)
    no_pgs = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, null=True)
    price = models.IntegerField(default=1000)
    cover_photo = models.ImageField(upload_to='books_photos', default='fed 1.jpg')

    '''
    Equivalent sql query of above code
    create table books(
    id int primary key autoincrement,
    name varchar(30),
    no_pgs int,
    author varchar(20)
    );
    '''
class AuthorPenName(models.Model):
    pen_name = models.CharField(max_length=56)
    author = models.OneToOneField(Author, on_delete=models.RESTRICT)

class Students(models.Model):
    name = models.CharField(max_length =20)
    roll = models.IntegerField()
    booked = models.ManyToManyField(Books)



    def __str__(self):
        return self.name






