
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from openai import OpenAI
from django.conf import settings

from django.http import HttpResponse
from django.shortcuts import render
from .models import userData,borrowerDetails,AddBook,ReviewList
from django.contrib import messages
from django.shortcuts import redirect,get_object_or_404

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, Http404
import os
from django.conf import settings
# from django.contrib.auth import authenticate, login as auth_login




# Create your views here.



# def allBooks(request):
#     return render(request,'all.html')




# remove api parts




def allBooks(request):
    books = AddBook.objects.all()  # fetch all books from DB
    return render(request, 'all.html', {'books': books})


def loginpage(request):
    return render(request,'login.html')

def signUpPage(request):
    return render(request,'signup.html')
from django.contrib.auth.models import User

def signUp(request):
    fullname = request.GET.get('fullname')
    uname = request.GET.get('username')
    pswd = request.GET.get('password')

    # Create Django Auth User
    if not User.objects.filter(username=uname).exists():
        user = User.objects.create_user(username=uname, password=pswd)
        user.save()
    else:
        return render(request, "signup.html", {"message": "Username already exists!"})

    # Store additional info in your userData table
    userdb = userData.objects.create(fullname=fullname, username=uname, password=pswd)

    return render(request, "login.html", {"message": "Account created successfully! Please login."})


def login(request):
    uname = request.GET.get('username')
    pswd = request.GET.get('password')
    
    user = authenticate(request, username=uname, password=pswd)
    
    if user is not None:
        auth_login(request, user)  # ✅ logs user properly
        return redirect(f"/?message={uname}")
    else:
        return render(request,'login.html',{'message' : 'Invalid Username or Password'})
    
    
    
        
    


def moreReviews(request):
    return render(request,'reviews.html')

def backToHome(request):
    message = request.GET.get('message', '') 
    books = AddBook.objects.all()
    reviews = ReviewList.objects.all().order_by('-id')[:3]
    return render(request,'index.html',{'books':books, 'reviews': reviews,'message': message})


def addBorrowerDetails(request):
    
    if request.method  == "POST":
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phno = request.POST.get('phno')
        dob = request.POST.get('dob')
        borrowdate = request.POST.get('borrowdate')
        returndate = request.POST.get('returndate')
        
        if not userData.objects.filter(username = username).exists():
            return render(request,'signup.html',{'message':"You are not registered ! please sign up first"})
        
        borrowerDetails.objects.create(
            username = username ,
			fullname = fullname,
			email = email,
			phoneno = phno,
			dob = dob,
			borrowDate = borrowdate,
			returnDate = returndate
   
		)
        return render(request,'index.html',{'message': "Book Borrowed successfully!"})

    
    return render(request,'index.html')



def list_book(request):
    books = AddBook.objects.all()
    return render(request,'index.html',{'books':books})



def addBooks(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author =request.POST.get('author')
        photo = request.FILES.get('photo')
        book_file = request.FILES.get('book_file')
        description = generate_description(title, author)
        
        AddBook.objects.create(title = title,author = author ,photo = photo,book_file=book_file,description = description)
        
        print("Generated description:", description)
        
    books = AddBook.objects.all()
    return render(request,'index.html',{'books':books})

        
def reviewPage(request):
    return render(request,'add_reviews.html')

def all_review_page(request):
    reviews = ReviewList.objects.all()

    return render(request,'reviews.html',{'reviews':reviews})


def add_review(request):
    if request.method == "POST":
        username = request.POST.get('username')
 # correct username
        
        book_title = request.POST.get('book_title')
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')
        
        ReviewList.objects.create(
            username=username,
            book_title=book_title,
            review_text=review_text,
            rating=rating  
        )
        return redirect('home')
    
    return redirect('home')





def home(request):
    message = request.GET.get('message', '') 
    books =AddBook.objects.all()   # your book model
    reviews = ReviewList.objects.all().order_by('-id')[:3]
    return render(request, 'index.html', {'books': books, 'reviews': reviews,'message':message})


def buyingPage(request,id):
    book = AddBook.objects.get(id = id)
    return render(request,'buybook.html', {'book':book})

def lendingPage(request,id):
    book = AddBook.objects.get(id=id)
    return render(request,'lendbook.html',{'book':book})





def generate_description(title, author):
    from openai import OpenAI
    import os
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    prompt = f"Write a short engaging book description for a book titled '{title}' by {author}."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80
        )

        # Check if response has the correct structure
        if response.choices and len(response.choices) > 0:
            # Depending on SDK version, you may need:
            # description = response.choices[0].message['content']
            description = response.choices[0].message.content
            return description.strip()
        else:
            return f"A wonderful book titled '{title}' by {author}."
    
    except Exception as e:
        print("Error generating description:", e)
        # fallback description if API fails
        return f"A wonderful book titled '{title}' by {author}."




def borrowerPage(request):
    return render(request,'borrowerdetails.html')




def download_book(request, book_id):
    try:
        book = AddBook.objects.get(id=book_id)
        if not book.book_file:
            raise Http404("Book file not found.")
        
        file_path = book.book_file.path
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    except AddBook.DoesNotExist:
        raise Http404("Book does not exist.")
    
    
    
    
    
from datetime import datetime, timedelta
from django.utils import timezone




@login_required
def lendBook(request, book_id):
    from django.utils import timezone
    from datetime import timedelta

    book = get_object_or_404(AddBook, id=book_id)

    if request.method == "POST":
        days = request.POST.get('customDays') or request.POST.get('duration')
        days = int(days)
        price = int(request.POST.get('price', 0))

        borrow_date = timezone.now().date()
        return_date = borrow_date + timedelta(days=days)

        # Get fullname from userData table
        try:
            userdata = userData.objects.get(username=request.user.username)
            fullname = userdata.fullname
        except userData.DoesNotExist:
            fullname = request.user.username

        # Check if borrowerDetails record already exists for this user
        borrower, created = borrowerDetails.objects.update_or_create(
            username=request.user.username,
            defaults={
                'fullname': fullname,
                'email': request.user.email,  # can update email
                'phoneno': "",  # optional
                'dob': timezone.now().date(),  # optional placeholder
                'borrowDate': borrow_date,
                'returnDate': return_date
            }
        )

        # Redirect to read page
        return redirect('read_lent_book', book_id=book.id, username=request.user.username)

    return render(request, 'lendbook.html', {'book': book})



@login_required
def read_lent_book(request, book_id, username):
    try:
        borrow_record = borrowerDetails.objects.get(username=username, borrowDate__lte=timezone.now().date(),
                                                     returnDate__gte=timezone.now().date())
        book = AddBook.objects.get(id=book_id)
        return render(request, 'read_lent_book.html', {'book': book})
    except borrowerDetails.DoesNotExist:
        return HttpResponse("Sorry, your access to this book has expired or you haven't borrowed it.")













