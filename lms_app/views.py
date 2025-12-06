from itertools import count, filterfalse
# from lib2to3.fixes.fix_input import context
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import *


@never_cache
@login_required(login_url='/login')
def home(request):
    return render(request, "home.html", context={"current_tab": "home", "usercount": (reader.objects.count()),
                                                 "bookcount": (book.objects.count()),
                                                 "issuedbookcount": (issuedboook.objects.count()),
                                                 "defaultercount": issuedboook.objects.filter(
                                                     due_date__lt=timezone.now(), is_returned=False).count()})


def readerhome(request):
    return render(request, "readerhome.html",
                  context={"current_tab": "readerhome", "usercount": (reader.objects.count()),
                           "bookcount": (book.objects.count()),
                           "issuedbookcount": (issuedboook.objects.count()),
                           "defaultercount": issuedboook.objects.filter(
                               due_date__lt=timezone.now(), is_returned=False).count()})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')

        if (username == "") or (pass1 == ""):
            messages.error(request, "Please Enter Both UserID and Password!!!")
            return redirect('/login')

        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            auth_login(request, user)
            try:

                messages.success(request, "Successfully Logged In")
                if username == "SuperAdmin" and pass1 == "admin1391":
                    return redirect('/home')
                else:
                    my_reader = reader.objects.get(reader_id=username)
                    request.session['reader_id'] = my_reader.reader_id
                    return redirect('/readerhome')

            except reader.DoesNotExist:
                messages.error(request, "Reader not found.")
                return redirect('/login')

        else:
            messages.error(request, "Username or Password is incorrect!!!")
            return redirect('/login')

    return render(request, 'login.html', context={})


def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if (uname == "") or (email == "") or (pass1 == "") or (pass2 == ""):
            messages.error(request, "!!! Please fill up all the inputs !!!")
            return redirect('/signup')

        else:
            checkUserID = all(char.isalpha() or char.isspace() for char in uname)
            if not checkUserID:
                memberIDcheck = reader.objects.filter(reader_id=uname)
                if memberIDcheck:
                    memberEmailcheck = reader.objects.filter(reader_email=email)
                    if memberEmailcheck:
                        memberCheck = reader.objects.filter(reader_id=uname, reader_email=email)
                        if memberCheck:
                            if pass1 != pass2:
                                messages.error(request, "!!! Password And Confirm-Password Did Not Matched !!!")
                                return redirect('/signup')
                            else:
                                userCheck = User.objects.filter(username=uname, email=email)
                                if userCheck:
                                    messages.error(request,
                                                   "Opps!!! You Have Already Created An Account. Please Log-In Now.")
                                    return redirect('/signup')
                                else:
                                    my_user = User.objects.create_user(uname, email, pass1)
                                    my_user.save()
                                    messages.success(request, "Successfully Signed Up !!!")
                                    return redirect('/login')
                        else:
                            messages.error(request, "Sorry!!! You Are Not A Registered Member Of The Library.")
                            return redirect('/signup')
                    else:
                        messages.error(request,
                                       "Please Use Daffodil International University Library Provided Registered Member Email.")
                        return redirect('/signup')
                else:
                    messages.error(request,
                                   "Please Use Daffodil International University Library Provided Registered Member ID.")
                    return redirect('/signup')
            else:
                messages.error(request, "User ID Contains Only Digits or (-)")
                return redirect('/signup')

    return render(request, 'signup.html', context={})


def readers(request):
    if request.method == 'POST':
        readerid = request.POST.get('readerid')
        readername = request.POST.get('readername')
        readeremail = request.POST.get('readeremail')
        dept = request.POST.get('dept')
        batch = request.POST.get('batch')
        contact = request.POST.get('contact')

        if (readerid == "") or (readername == "") or (readeremail == "") or (dept == "") or (batch == "") or (
                contact == ""):
            messages.error(request, "!!! Please Fill up All The Input Fields !!!")
            return redirect('/readers')

        else:
            checkReadeid = all(char.isdigit() or char == '-' for char in readerid)
            checkReadername = all(char.isalpha() or char.isspace() or char == '.' for char in readername)

            if checkReadeid:

                if checkReadername:

                    if '@' in readeremail:
                        parts = readeremail.split('@', maxsplit=2)

                        if parts[1] == "diu.edu.bd":
                            newreader = reader.objects.create(reader_id=readerid, reader_name=readername,
                                                              reader_email=readeremail, reader_contact=contact,
                                                              reader_dept=dept, reader_batch=batch)
                            newreader.save()

                            messages.success(request, "Successfully Added A New Reader.")
                            return redirect('/readers')
                        else:
                            messages.error(request,
                                           "Please Use DIU Provided Email Address ex (hasan22205101391@diu.edu.bd).")
                            return redirect('/readers')
                    else:
                        messages.error(request, "!!! Invalid Email Address Type !!!")
                        return redirect('/readers')

                else:
                    messages.error(request, "!!! Reader Name Contains Only Letters, Space and (.) !!!")
                    return redirect('/readers')
            else:
                messages.error(request, "!!! Reader ID Contains Only Digits and/or (-) !!!")
                return redirect('/readers')

    my_reader = reader.objects.all()
    return render(request, "readers.html",
                  context={"current_tab": "readers", "my_reader": my_reader})


def books(request):
    if request.method == "POST":
        bookid = request.POST.get('bookid')
        bookname = request.POST.get('bookname')
        author = request.POST.get('author')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')

        checkBookname = all(char.isalpha() or char.isspace() for char in bookname)
        checkAuthorname = all(char.isalpha() or char.isspace() for char in author)

        if (bookid == "") or (bookname == "") or (author == "") or (category == "") or (quantity == ""):
            messages.error(request, "Please fill up all the inputs!!!")
            return redirect('/books')
        else:
            if checkBookname:
                if checkAuthorname:
                    if int(quantity) <= 0:
                        messages.error(request, "Invalid Quantity. Please Use 1 or More as Books Quantity.")
                        return redirect('/books')
                    else:
                        add_books = book.objects.create(bookid=bookid, bookname=bookname, author=author,
                                                        category=category, quantity=quantity)
                        add_books.save()

                        messages.success(request, "Successfully Added The Book")
                        return redirect('/books')
                else:
                    messages.error(request, "Author Name Must Be Contains Only letter Nothing Else.")
                    return redirect('/books')
            else:
                messages.error(request, "Book Name Must Be Contains Only letter Nothing Else.")
                return redirect('/books')

    last_book = book.objects.order_by('-id').first()
    last_book_id = last_book.bookid if last_book else ''
    all_books = book.objects.all()
    return render(request, "books.html", context={
        "current_tab": "books",
        "all_books": all_books,
        "last_book_id": last_book_id
    })


def readerbooks(request):
    all_books = book.objects.all()
    return render(request, "readerbooks.html", context={
        "current_tab": "readerbooks",
        "all_books": all_books
    })


def returns(request):
    if request.method == "POST":
        reader_id = request.POST.get('readerid')
        book_id = request.POST.get('bookid')

        checkReaderid = all(char.isdigit() for char in reader_id)
        checkBookid = all(char.isdigit() for char in book_id)

        if checkReaderid:
            if checkBookid:
                try:
                    if (issuedboook.objects.count() == 0):
                        messages.error(request, "There Are No Books To Be Returned.")
                        return redirect('/returns')
                    else:
                        try:
                            issued_book = issuedboook.objects.get(reader_id=reader_id, bookid=book_id,
                                                                  is_returned=False)
                            issued_book.is_returned = True
                            issued_book.save()

                            book_instance = get_object_or_404(book, bookid=book_id)
                            book_instance.quantity += 1
                            book_instance.save()

                            messages.success(request, "Book returned successfully!")
                            return redirect('/returns')
                        except issuedboook.DoesNotExist:
                            messages.error(request, "This book has already been returned.")
                            return redirect('/returns')

                except issuedboook.DoesNotExist:
                    messages.error(request, "Issued book record not found.")
            else:
                messages.error(request, "Book ID Contains Only Digits")
                return redirect('/returns')
        else:
            messages.error(request, "Reader ID Contains Only Digits")
            return redirect('/returns')

    return render(request, "returns.html", context={"current_tab": "returns",
                                                    "issuedboookdetails": issuedboook.objects.filter(
                                                        is_returned=False)})


def bookIssue(request):
    if request.method == "POST":
        reader_id = request.POST.get('readerid')
        reader_name = request.POST.get('readername')
        reader_email = request.POST.get('email')
        book_id = request.POST.get('bookid')
        book_name = request.POST.get('bookname')
        author = request.POST.get('author')

        checkReaderid = all(char.isdigit() for char in reader_id)
        checkBookid = all(char.isdigit() for char in book_id)

        if checkReaderid:
            if checkBookid:
                try:
                    if (reader.objects.count() == 0) or (book.objects.count() == 0):
                        messages.error(request, "Sorry there are no readers or books registered in library yet.")
                        return redirect('/bookIssue')
                    else:
                        readerCheck = issuedboook.objects.filter(reader_id=reader_id, bookid=book_id, is_returned=False)
                        if readerCheck:
                            messages.error(request, "This Reader Already Issued The Book and Did not Returned It Yet.")
                            return redirect('/bookIssue')
                        else:
                            book_instance = book.objects.get(bookid=book_id)
                            if book_instance.quantity > 0:
                                issued_book = issuedboook.objects.create(
                                    reader_id=reader_id,
                                    reader_name=reader_name,
                                    reader_email=reader_email,
                                    bookid=book_id,
                                    bookname=book_name,
                                    author=author,
                                )
                                issued_book.save()

                                book_instance.quantity -= 1
                                book_instance.save()

                                messages.success(request, "Successfully Issued The Book To The Reader.")
                                return redirect('/bookIssue')
                            else:
                                messages.error(request, "Sorry!!! This Is Not Available At The Time.")
                                return redirect('/bookIssue')
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)})
            else:
                messages.error(request, "Book ID Contains Only Digits")
                return redirect('/bookIssue')
        else:
            messages.error(request, "Reader ID Contains Only Digits")
            return redirect('/bookIssue')
    return render(request, "bookIssue.html",
                  context={"current_tab": "bookIssue", "issuedboookdetails": (issuedboook.objects.all())})


def readerbookIssue(request):
    reader_id = request.session.get('reader_id')

    if reader_id:
        issued_books = issuedboook.objects.filter(reader_id=reader_id)
    else:
        issued_books = []

    return render(request, "readerbookIssue.html", context={
        "current_tab": "readerIssuedbooks",
        "issuedboookdetails": issued_books,
    })


def defaulter(request):
    defaulters = issuedboook.objects.filter(due_date__lt=timezone.now(), is_returned=False)
    return render(request, "defaulter.html", context={"current_tab": "defaulter", "defaulters": defaulters})


def readerReport(request):
    reader_id = request.session.get('reader_id')

    if not reader_id:
        return redirect('/login')

    unreturned_books = issuedboook.objects.filter(reader_id=reader_id, due_date__lt=timezone.now(), is_returned=False)
    return render(request, 'readerReport.html',
                  context={"current_tab": "readerReport", 'unreturned_books': unreturned_books})

@never_cache
def logout_view(request):
    logout(request)
    request.session.clear()
    response = redirect('/login')
    response.delete_cookie('sessionid')
    return response


def get_reader_info(request):
    reader_id = request.GET.get('reader_id')
    try:
        readers = reader.objects.get(reader_id=reader_id)
        data = {
            'reader_name': readers.reader_name,
            'reader_email': readers.reader_email,
        }
    except readers.DoesNotExist:
        data = {
            'reader_name': '',
            'reader_email': '',
        }
    return JsonResponse(data)


def get_book_info(request):
    book_id = request.GET.get('book_id')
    try:
        books = book.objects.get(bookid=book_id)
        data = {
            'book_name': books.bookname,
            'author': books.author,
        }
    except book.DoesNotExist:
        data = {
            'book_name': '',
            'author': '',
        }
    return JsonResponse(data)


def readers_list(request):
    query = request.GET.get('search')
    if query:
        readers = reader.objects.filter(reader_id__icontains=query)
    else:
        readers = reader.objects.all()

    return render(request, 'readers.html', context={"current_tab": "readers", 'readers': readers, 'query': query})


def books_list(request):
    query = request.GET.get('search')
    if query:
        books = book.objects.filter(bookid__icontains=query)
    else:
        books = book.objects.all()

    return render(request, 'books.html', context={"current_tab": "books", 'books': books, 'query': query})


def readerbooks_list(request):
    query = request.GET.get('readersearch')
    if query:
        books = book.objects.filter(bookid__icontains=query)
    else:
        books = book.objects.all()

    return render(request, 'readerbooks.html', context={"current_tab": "readerbooks", 'books': books, 'query': query})


def issuedbooks_list(request):
    query = request.GET.get('issuedbooksearch')
    if query:
        records = issuedboook.objects.filter(reader_id__icontains=query)
    else:
        records = issuedboook.objects.all()

    return render(request, 'bookissue.html', context={"current_tab": "bookIssue", 'records': records, 'query': query})


def readerissuedbooks_list(request):
    query = request.GET.get('readerissuedbooks')
    if query:
        records = issuedboook.objects.filter(bookid__icontains=query)
    else:
        records = issuedboook.objects.all()

    return render(request, 'readerbookissue.html',
                  context={"current_tab": "readerIssuedbooks", 'records': records, 'query': query})
