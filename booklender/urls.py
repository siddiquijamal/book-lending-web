from django.contrib import admin
from django.urls import path,include
from booklender import views
from django.conf.urls.static import static

from books import settings

urlpatterns = [
    # path('', views.list_book, name='home'),  # <-- MAKE THIS FIRST
    path('', views.home, name='home'),


    path('allbooks/',views.allBooks,name = 'allbooks'),
    path('loginpage/',views.loginpage, name ='loginpage'),
    path('signuppage/',views.signUpPage, name = 'signuppage'),
    path('morereviews/',views.moreReviews,name = 'morereviews'),
    path('backtohome/',views.backToHome,name = 'backtohome'),
    path('signup/',views.signUp,name = "signup"),
    path('login/',views.login,name = 'login'),
    path('borrowerdetails/',views.addBorrowerDetails),
    path('list_books/',views.list_book),
    path('addbooks/',views.addBooks, name = 'addbooks'),
    path('reviewpage/',views.reviewPage,name = 'reviewpage'),
    path('addreview/',views.add_review, name = "addreview"),
    # path('homepage/',views.home)
    # path('editreview/<int:id>/',views.editreview,name = 'editreview'),
    path('allreview/',views.all_review_page,name = "allreviews"),
    # path('buyingpage/',views.buyingPage, name = 'buyingpage'),
    path('lendingpage/<int:id>/',views.lendingPage, name = 'lendingpage'),
    path('buyingpage/<int:id>/', views.buyingPage, name='buyingpage'),
    path('borrowerpage/',views.borrowerPage,name = 'borrowerpage'),
    path('download/<int:book_id>/', views.download_book, name='download_book'),
    path('lendbook/<int:book_id>/', views.lendBook, name='lendBook'),
    path('readlentbook/<int:book_id>/<str:username>/', views.read_lent_book, name='read_lent_book'),
    
    
    # rest api parts 
    





    
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
