
from django.urls import path
from lib_mgmt_sys import views

app_name = 'lms'

urlpatterns = [
    #/lms/list_books/   (user le hannu parne urls)
    path('list_books/', views.list_books, name='list_books'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_books/', views.add_books, name='add_books'),
    path('edit_books/<int:id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:id>/', views.delete_book, name='delete_book'),
    path('list_author/', views.ListAuthor.as_view(), name='list_author'),
    path('about_us/', views.AboutUsView.as_view(), name= 'about_us'),
    path('list_books1/', views.BookListView.as_view(), name='list_books1'),
    path('add_author_generic/', views.AddAuthorGeneric.as_view(), name='add_author_generic'),
    path('edit_author/<int:pk>/', views.UpdateAuthorView.as_view(), name='update_author'),
    path('detail_author/<int:pk>/', views.AuthorDetailView.as_view(), name='detail_author'),
    path('delete_author/<int:pk>/', views.AuthorDeleteView.as_view(), name='delete_author'),
    path('login/', views.LoginUserView.as_view(), name='lms_login'),
    path('logout/', views.LogOutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name= 'register'),
    path('book_api/', views.CsrfBookAPI, name= 'book_api'),
    path('book_api/<int:id>/', views.CsrfBookObjectAPI, name= 'bookobject_api'),
    path('send_email/', views.send_email, name= 'send_email'),
    path('search/<str:model>/', views.search_view, name= 'search')
]