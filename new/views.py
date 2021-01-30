from django import forms
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, Add_BookForm
from .decorators import *
from django.http import HttpResponseRedirect, HttpResponse
from .forms import Add_BookForm, IssuedForm, ContactForm
from .models import *
from .filters import BookFilter
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta, date
from django.contrib.auth.models import User
from django.core.mail import send_mail
from djangoProject.settings import EMAIL_HOST_USER


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # log user in
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account has been created successfully')
            return redirect('user_home')
    else:
        form = SignUpForm()
    context = {'s_form': form}
    return render(request, 'signup.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_home')
        else:
            messages.info(request, "Username OR password is incorrect")
    context = {}
    return render(request, 'login_user.html', context)


def logout_user(request):
    logout(request)
    return redirect('login_user')


def login_admin(request):
    if request.method == 'POST':
        user_ID = request.POST.get('user_ID')
        username = request.POST.get('username')
        password = request.POST.get('password')
        superuser = request.POST.get(User.is_superuser)
        admin = authenticate(request, user_ID=user_ID, username=username, password=password, superuser=superuser)
        if admin is not None:
            login(request, admin)
            return redirect('admin_home')
        else:
            messages.info(request, "Credentials incorrect")

    context = {}
    return render(request, 'login_admin.html', context)


def logout_admin(request):
    logout(request)
    return redirect('login_admin')


@login_required(login_url='login_user')
def homepage_user(request):
    books = Add_Book.objects.filter(status='Not Issued')
    myfilter = BookFilter(request.GET, queryset=books)
    books = myfilter.qs
    context = {'books': books, 'myfilter': myfilter}
    return render(request, 'homepage_user.html', context=context)


@login_required(login_url='login_admin')
def homepage_admin(request):
    books = Add_Book.objects.all()
    myfilter = BookFilter(request.GET, queryset=books)
    books = myfilter.qs
    context = {'books': books, 'myfilter': myfilter}
    return render(request, 'homepage_admin.html', context=context)


@login_required(login_url='login_admin')
def add_book(request):
    form = Add_BookForm()
    if request.method == 'POST':
        form = Add_BookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_book')
    context = {'form': form}
    return render(request, 'add_book.html', context)


@login_required(login_url='login_admin')
def update_book(request, pk):
    book = Add_Book.objects.get(id=pk)
    form = Add_BookForm(instance=book)
    if request.method == 'POST':
        form = Add_BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('/homepage_admin')

    context = {'form': form}
    return render(request, 'add_book.html', context)


@login_required(login_url='login_admin')
def delete_book(request, pk):
    book = Add_Book.objects.get(id=pk)
    if request.method == "POST":
        book.delete()
        return redirect('/homepage_admin')
    context = {'book': book}
    return render(request, 'delete_book.html', context)


def queryset(args):
    pass


@login_required(login_url='login_admin')
def issue_book(request):
    form = IssuedForm(request.POST or None)
    if request.method == 'POST':
        form = IssuedForm(request.POST)
        if form.is_valid():
            def no_books():
                with connection.cursor() as cursor:
                    cursor.execute("select u.username, count(i.user_id) from new_issued i, auth_user u where "
                                   "i.user_id=u.id group by user_id")
                    record = cursor.fetchall()
                    for i in record:
                        if i[1] == 2 and i[0] == Issued.user:
                            messages.warning('This user has already borrowed 2 books')
                            return redirect('/issue_book')
                        else:
                            instance = form.save(commit=False)
                            instance.save()
                            messages.success(request, 'Book was issued successfully')
                            return HttpResponseRedirect('/issue_book')
            no_books()

    else:  # GET request method
        form = IssuedForm()
    context = {'form': form}

    def status():
        s = 'Issued'
        with connection.cursor() as cursor:
            cursor.execute("SELECT book_id FROM new_issued")
            record = cursor.fetchall()
            for i in record:
                cursor.execute("UPDATE new_add_book SET status=%s WHERE id=%s", [s, i])
                row = cursor.fetchall()
                for j in row:
                    return j

    status()
    return render(request, 'issue.html', context)


@login_required(login_url='login_admin')
def issue_views(request):
    return render(request, 'issue_view.html')


@login_required(login_url='login_admin')
def user_status(request):
    issues = Issued.objects.all()
    context = {'issues': issues}
    return render(request, 'user_status.html', context)


@login_required(login_url='login_admin')
def return_book(request, pk):
    issued = Issued.objects.get(id=pk)
    if request.method == "POST":
        issued.delete()
        return redirect('/homepage_admin')
    context = {'issued': issued}

    def status():
        s = 'Not Issued'
        with connection.cursor() as cursor:
            cursor.execute("SELECT book_id FROM new_issued")
            record = cursor.fetchall()
            for i in record:
                cursor.execute("UPDATE new_add_book SET status=%s WHERE id=%s", [s, i])
                row = cursor.fetchall()
                for j in row:
                    return j

    status()
    return render(request, 'return_book.html', context)


@login_required(login_url='login_user')
def issued_user(request):
    issues = Issued.objects.filter(user=request.user)
    li1 = []
    li2 = []
    for ib in issues:
        books = Add_Book.objects.filter(Book_Name=ib.book)
        for book in books:
            t = (ib.user, book.Book_Name, book.Author)
            li1.append(t)
        issdate = str(ib.issue_date.day) + '-' + str(ib.issue_date.month) + '-' + str(ib.issue_date.year)
        expdate = str(ib.expiry_date.day) + '-' + str(ib.expiry_date.month) + '-' + str(ib.expiry_date.year)
        # fine calculation
        days = (date.today() - ib.issue_date)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d - 15
            fine = 'Rs.' + str(day * 5)
        t = (issdate, expdate, fine)
        li2.append(t)
    return render(request, 'issued_user.html', {'li1': li1, 'li2': li2})


def contact_view(request):
    sub = ContactForm()
    if request.method == 'POST':
        sub = ContactForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['email']
            name = sub.cleaned_data['name']
            message = sub.cleaned_data['message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['smriti.project12@gmail.com'], fail_silently = False)
            messages.success(request, "Feedback sent successfully! We will look into it immediately")
    return render(request, 'contact.html', {'form': sub})
