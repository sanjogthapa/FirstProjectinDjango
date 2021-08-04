from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.shortcuts import HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, DetailView, UpdateView
from rest_framework.parsers import JSONParser

from lib_mgmt_sys.models import *
from lib_mgmt_sys.forms import *
from django import views

from lib_mgmt_sys.serializer import BookSerializer


def is_librarian(user):
    return user.groups.filter(name= 'Librarian').exists()

# Create your views here.
def sample_view(request):
    # return HttpResponse('Hi, i am a view')
    user = 'shreyansh'
    friends = ['ram', 'sita', 'hari', 'gita']
    return render(request,'index.html', context = {'user_name': user, 'friends': friends})

def gallery(request):

    return render(request, 'gallery.html')


@login_required(login_url=reverse_lazy('lms:lms_login'))
def list_books(request):
    books = Books.objects.all()
    return render(request, 'lms/list_books.html', context={'books': books})


@login_required(login_url=reverse_lazy('lms:lms_login'))
def add_author(request):
    if request.method == 'GET':
        author_add_form= AuthorAddForm()
        return render(request,'lms/add_author.html', context={'form': author_add_form})
    elif request.method == 'POST':
        name = request.POST['name']   #request.post ma dictionary ma data aaune vayera
        age = request.POST.get('age')
        #saving the above info in the database
        author = Author.objects.create(name=name, age=age)
        #yesari gare ni huncha

        # a= Author()
        # a.name= name
        # a.age= age
        # a.save()
        return HttpResponse('Author Saved in db')


@login_required(login_url=reverse_lazy('lms:lms_login'))
def add_books(request):
    if request.method == 'GET':
        book_form = BookModelForm()
        return render(request,'lms/add_books.html',{'book_form': book_form})
    else:
        book_form= BookModelForm(request.POST, request.FILES)
        if book_form.is_valid():
            book_form.save()
            return redirect('lms:list_books')
        else:
            return render(request,'lms/add_books.html',{'book_form': book_form})



@login_required(login_url='/lms/login/')
@user_passes_test(is_librarian, login_url=reverse_lazy('lms:lms_login'))
def edit_book(request,id):
    book = Books.objects.get(id=id)
    if request.method == 'GET':
        form = BookModelForm(instance=book)
        return render(request, 'lms/edit_book.html', {'form': form})
    elif request.method == 'POST':
        form = BookModelForm(request.POST, instance = book)
        if form.is_valid():
            form.save()
            return redirect('lms:list_books')
        else:
            return render(request, 'lms/edit_book.html', {'form': form})

@login_required(login_url='/lms/login/')
def delete_book(request,id):
    book = Books.objects.get(id=id)
    book.delete()
    return redirect('lms:list_books')



class ListAuthor(LoginRequiredMixin,views.View):
    login_url = reverse_lazy('lms:lms_login')

    def get(self, request):
        author= Author.objects.all()
        return render(request, 'lms/list_author.html', {'author_list': author})



class AddAuthor(LoginRequiredMixin,views.View):
    login_url = reverse_lazy('lms:lms_login')
    def get(self, request):
        author_add_form = AuthorAddForm()
        return render(request, 'lms/add_author.html', context={'form': author_add_form})

    def post(self,request):
        name = request.POST['name']  # request.post ma dictionary ma data aaune vayera
        age = request.POST.get('age')
        # saving the above info in the database
        author = Author.objects.create(name=name, age=age)
        return HttpResponse('Author saved in db')

"""
GENERIC VIEWS
-> Template view
-> List View
->Create View
-> Update View
-> Delete View
->Detail View
"""

class AboutUsView(TemplateView):
     template_name = 'lms/about_us.html'

     def get_context_data(self):
         return {'phone_no': 9849150687}



class ContactUsView(TemplateView):
    template_name = 'lms/contact_us.html'



class BookListView(ListView):
    model = Books
    template_name = 'lms/list_books.html'
    context_object_name = 'books'

"""
Create generic view
"""
class AddAuthorGeneric(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('lms:lms_login')
    model = Author
    template_name = 'lms/add_author_generic.html' #<app_name>/<model_name>_create.html (default location yesto huncha)
    fields = '__all__'    #('name',) (single fields lyauna yestari lekhhne)
    success_url = reverse_lazy('lms:list_author')
    #form_class = BookModelForm


class UpdateAuthorView(LoginRequiredMixin,UpdateView):
    login_url = '/lms/login/'
    model = Author
    fields = '__all__'
    template_name = 'lms/update_author.html'
    success_url = reverse_lazy('lms:list_author')

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return Author.objects.get(id= id)


class AuthorDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('lms:lms_login')
    model = Author
    template_name = 'lms/author_detail.html'


class AuthorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = reverse_lazy('lms:lms_login')
    model = Author
    template_name = 'lms/delete_author.html'
    success_url = reverse_lazy('lms:list_author')


    def test_func(self):
        return self.request.user.groups.filter(name = 'Librarian').exists()

    def handle_no_permission(self):
        return redirect('lms:list_author')



class LoginUserView(views.View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'lms/login.html',{'login_form': login_form})

    def post(self, request):
        username= request.POST.get('username')
        password= request.POST.get('password')
        user= authenticate(username=username, password= password)
        if user is None:
            return redirect('lms:lms_login')
        else:
            if user.is_active:
                login(request, user=user)
                return redirect('lms:list_books')
            else:

                return redirect('lms:lms_login')


class LogOutUserView(views.View):
    def get(self, request):
        logout(request)
        return redirect('lms:list_books')



class RegisterUserView(views.View):
    def get(self, request):
        user_form= UserModelForm
        return render(request, 'lms/register.html', {'form':user_form})

    def post(self, request):
        user_form = UserModelForm(request.POST)
        if user_form.is_valid():
            user= user_form.save()
            user.set_password(user.password)
            user.save()
            student_group= Group.objects.get(name= request.POST['role'])
            user.groups.add(student_group)
            login(request, user)
            return redirect('lms:list_books')



class BookAPI(views.View):
    def get(self, request):
        BookQs= Books.objects.all()
        ser= BookSerializer(BookQs, many=True)
        return JsonResponse(ser.data, safe= False)
    def post(self, request):
        data= JSONParser().parse(request)
        ser= BookSerializer(data= data)
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data)
        return JsonResponse(ser.errors, status=500)


class BookObjectAPI(views.View):

    def get(self, request, id):
        book = Books.objects.get(id=id)
        ser= BookSerializer(book)
        return JsonResponse(ser.data)

    def put(self,request,id):
        book = Books.objects.get(id=id)
        data = JSONParser().parse(request)
        ser = BookSerializer(book,data=data)
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data,status=200)
        return JsonResponse(ser.errors, status=500)

    def delete(self, request, id):
        book = Books.objects.get(id=id)
        book.delete()
        return HttpResponse(status=500)



def send_email(request):
    recipient_address = 'sanjogthapa319@gmail.com'
    send_mail(
        'Test Email',
        'Hello, \n This is a test message',
        'sanjogcrickter@gmail.com'
        [recipient_address],
        fail_silently = False
    )
    return HttpResponse('Email sent')


def search_view(request, model):
    if request.method == 'POST':
        if model == 'books':
            books = Books.objects.filter(Q(name__icontains=request.POST['search_text'] |
                                        Q(price = request.POST['search_text'])
                                           | Q(no_pgs= request.POST['search_text'])))

            return render(request, 'lms/list_books.html', {'books': books})
        else:
            author = Author.objects.filter(name__icontains=request.POST['search_text'])
            return render(request, 'lms/list_author.html', {'author_list': author})









CsrfBookAPI = csrf_exempt(BookAPI.as_view())
CsrfBookObjectAPI = csrf_exempt(BookObjectAPI.as_view())





