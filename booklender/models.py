from django.db import models
from PIL import Image
from django.contrib.auth.models import User



# Create your models here.

class userData(models.Model):
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100,primary_key=True)
    password = models.CharField(max_length=100)
    
    
    class Meta:
        db_table = 'userdata'
        
        
class borrowerDetails(models.Model):
    username = models.CharField(max_length=30)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100 ,unique=True)
    phoneno = models.CharField( max_length=15)
    dob = models.DateField()
    borrowDate= models.DateField()
    returnDate= models.DateField()
    
    
    def __str__(self):
        return self.fullname

    
    class Meta:
        db_table = 'borrowerdetails'    
        
        
class AddBook(models.Model):
    photo = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=40)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    book_file = models.FileField(upload_to='books/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    

class ReviewList(models.Model):
    username = models.CharField(max_length=100)
    book_title = models.CharField(max_length=200)
    review_text = models.TextField(max_length=500)
    rating = models.IntegerField(choices=[
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)  # <-- change here

    def __str__(self):
        return self.username





