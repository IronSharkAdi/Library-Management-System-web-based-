from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User , auth
from .models import booklist , booktaken , recordofediting , recofremoving , userprofile, permissions , borrower
from datetime import datetime 
from django.http import HttpResponse
import csv


def home(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        password = request.POST.get("password")
        user = User.objects.create_user(username=name, password=password, is_superuser = True )
        newuser = permissions()
        u = User.objects.get(username=name)
        newuser.user = u
        newuser.addbook = True
        newuser.addstaff = True
        newuser.editbooks = True
        newuser.editstaff = True
        newuser.recofredited = True
        newuser.recofdeleted = True
        newuser.removebook = True
        newuser.removestaff = True
        newuser.save()
        user1 = User()
        user1 = auth.authenticate(username = name , password=password)
        auth.login(request , user1)
        return redirect('/')

    else :
        count5 = User.objects.filter(last_login__startswith=datetime.now().date()).count()
        count= booklist.objects.all().count()
        count1= User.objects.all().count()
        count2 = borrower.objects.all().count()
        newuser = False
        if count1 == 0:
            newuser = True
        return render(request, 'index.html' , {'count':count, 'count1':count1, 'count2':count2 ,'count5':count5 ,'newuser':newuser })

def login(request):
    if request.method == 'POST':
        user = User()
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = auth.authenticate(username = username , password=password)
        if user is not None:
            auth.login(request , user)
            return redirect('/')
        else:
            messages.info(request , 'Invalid User')
            return redirect('login')

    else:
        notFound = True
        return render(request, 'login.html' ,{'notFound':notFound}) 


def logout(request):
    auth.logout(request)
    return redirect('/')

def query(request):
    return render(request , 'query.html')
def makeQuery(request):
    if request.method == 'GET': 
        details = []
        name = request.GET.get("searchedThis")
        details.append(name)
        for i in details:
            if i != "":
                searchedBy = request.GET.get("searchBy")
                if searchedBy == 'dispo':
                    searched = booklist.objects.all().filter(dispo__startswith=name)
                elif searchedBy == 'Buyer Name':
                    searched = booklist.objects.all().filter(buyerName__startswith=name)
                elif searchedBy == 'Location':
                    searched = booklist.objects.all().filter(location__startswith=name)
                elif searchedBy == 'Fabric Type-2':
                    searched = booklist.objects.all().filter(fabricType1__startswith=name)
                elif searchedBy == 'Fabric Type-2':
                    searched = booklist.objects.all().filter(fabricType2__startswith=name)
                elif searchedBy == 'Market Reference No.':
                    searched = booklist.objects.all().filter(marketReferenceNo__startswith=name)
            else:
                messages.info(request , 'What do you want me to do query with ?')
                return redirect('query')
        return render(request , 'makeQuery.html', {'searched':searched ,'name':name, 'searchedBy':searchedBy})
def backhome(request):
    return redirect('/')
def querypage(request):
    return redirect('/query')


def addbook(request):
    count= booklist.objects.all().count()
    books = booklist.objects.all()
    if request.method == 'POST':
        addedbook = booklist()
        dispo = request.POST.get('dispo')
        if booklist.objects.filter(dispo=dispo).exists():
            messages.info(request , 'Book already exists')
            return redirect('addbook')
        else:        
            try:
                addedbook.img = request.FILES['image']
            except:
                pass
            addedbook.dispo = dispo
            addedbook.save()
            return redirect('/')
    else:
        return render(request, 'addbook.html')

def issue(request):
    if request.method == 'POST' and 'submit' in request.POST:
        name = request.POST.get('name')
        number = request.POST.get('number')
        dispo = request.POST.get('bookdispo')
        details = []
        details.append(name)
        details.append(number)
        details.append(dispo)
        for i in details:
            if i == "":
                messages.info(request , 'All fields are required')
                return redirect('issue')
        try:
            number = int(number)
        except:
            messages.info(request, "Number doesn't contains letters")
            return redirect('issue')
        book = booktaken()
        members = borrower.objects.all().count()
        name = request.POST.get('name')       
        if booklist.objects.filter(dispo=dispo).exists():
            thatbook = booklist.objects.get(dispo=dispo)
            if thatbook.borrowed_book == False:
                if members > 0:
                    if borrower.objects.filter(name=name).exists():
                        man = borrower.objects.get(name=name)
                    else:
                        man = borrower()
                        man.name = request.POST.get('name')
                        man.number = request.POST.get('number')
                else:
                    man = borrower()
                    man.name = request.POST.get('name')
                    man.number = request.POST.get('number')
                book.bookdispo = dispo
                book.borrower = man
                book.taken_at =  datetime.now()
                thatbook.borrowed_book = True
                thatbook.save()
                man.save()
                book.save()
            
                return redirect('/')                 
            else:
                messages.info(request , 'The book is already borrowed')
                return redirect('issue')                
        else:
            messages.info(request , 'book not found')
            return redirect('issue')

    elif request.method == 'POST' and 'refresh' in request.POST:
        name = request.POST.get('name')
        if name == "":
            messages.info(request , 'Write something at Name field')
            return redirect('issue')
        else:
            if borrower.objects.filter(name=name).exists():
                man = borrower.objects.get(name=name)
                return render(request , 'issueform.html' , {'man':man})
            else:
                messages.info(request , 'Borrower not found')
                return redirect('issue')
        return render(request, 'issueform.html', {})
    else:
        return render(request, 'issueform.html')
def bookrec(request):
    if request.method == 'POST':
        bookdispo = request.POST.get('bookdispo')
        details = []
        details.append(bookdispo)
        wrong = False
        for i in details:
            if i == "":
                wrong = True
                break
        if wrong == True:
            messages.info(request , 'Please , write the book dispo')
            return redirect('bookrec')
        else:
            if booklist.objects.filter(dispo=bookdispo).exists():
                found = booklist.objects.get(dispo=bookdispo)
                if found.borrowed_book == True:  
                    found.borrowed_book = False
                    x = booktaken.objects.get(bookdispo=bookdispo)
                    x.given_at = datetime.now()
                    found.save()
                    x.save()
                    return redirect('/')
                else:
                    messages.info(request , 'Book was never taken')
                    return redirect('bookrec')
            else:
                messages.info(request , "That book doesn't exists")
                return redirect('bookrec')
    else:
        return render(request, 'recbook.html')

def bookrecord(request):
    if request.method == 'GET': 
        details = []
        name = request.GET.get("searchedThis")
        details.append(name)
        for i in details:
            if i != "":
                searchedBy = request.GET.get("searchBy")
                
                searched = booktaken.objects.all().filter(bookdispo__startswith=name)        
                return render(request , 'bookrecord.html', {'searched':searched , 'name':name, 'searchedBy':searchedBy} )
            else:
                messages.info(request , 'What do you want me to do query with ?')
                return redirect('bookform')
    return render(request, 'bookrecord.html')

def bookform(request):
    return render(request , 'bookform.html')



def editbook(request):
    return render(request , 'editbookform.html')

def adduser(request):
    if request.method == "POST":
        details = []
        name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        details.append(name)
        details.append(password)
        wrong = False
        for i in details:
            if i == "":
                wrong = True
                break
        if wrong == True:
            messages.info(request , 'All fields are required')
            return redirect('adduser')
        else:
            try:
                if email == "":
                    user = User.objects.create_user(username=name, password=password)
                else:
                    user = User.objects.create_user(username=name, email=email, password=password)
                user.save()
                newuser = permissions()
                u = User.objects.get(username=name)
                newuser.user = u
                if "addbook" in request.POST:
                    newuser.addbook = True
                if "addstaff" in request.POST:
                    newuser.addstaff = True

                if "editbooks" in request.POST:
                    newuser.editbooks = True
                if "editstaff" in request.POST:
                    newuser.editstaff = True
                if "recofredited" in request.POST:
                    newuser.recofredited = True
                if "recofdeleted" in request.POST:
                    newuser.recofdeleted = True
                if "removebook" in request.POST:
                    newuser.removebook = True
                if "removestaff" in request.POST:
                    newuser.removestaff = True
                newuser.save()
                return redirect('/')
            except:
                messages.info(request , 'User already exists')
                redirect('adduser')
    return render(request , 'adduserform.html')


def removeuser(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name == "":
            messages.info(request, "*Please write any name")
            redirect("removeuser")
        else:
            try:
                user = User.objects.get(username=name)
                user.delete()
                return redirect('/')
            except:
                messages.info(request, "*User not found")
                redirect("removeuser")
    return render(request , 'removeuser.html')

def editbooksection(request):
    if request.method == 'GET': 
        details = []
        name = request.GET.get("searchedThis")
        details.append(name)
        for i in details:
            if i != "":
                searchedBy = request.GET.get("searchBy")
                if searchedBy == 'dispo':
                    searched = booklist.objects.all().filter(dispo__startswith=name)
            else:
                messages.info(request , '*What do you want me to do search with ?')
                return redirect('editbook')
        return render(request , 'editbooksection.html', {'searched':searched , 'name':name, 'searchedBy':searchedBy})

def edit(request ,search_dispo , name , searchedBy):
    object = booklist.objects.get(dispo=search_dispo)
    if request.method == "POST":
        newrec = recordofediting()
        newrec.bdispo = object.dispo
        object.dispo = request.POST.get('name')
        object.save()
        newrec.tdispo = request.POST.get('name')
        current_user = request.user
        newrec.editedby = current_user.username
        newrec.save()
        if searchedBy == 'dispo':
            searched = booklist.objects.all().filter(dispo__startswith=name)
        return render(request , 'editbooksection.html', {'searched':searched , 'name':name, 'searchedBy':searchedBy})
    else:
        return render(request, 'editform.html' , {'search_dispo':search_dispo , 'object':object})




def delete(request , search_id , name , searchedBy ):
    try:
        object = booklist.objects.get(id=search_id)
        newrec = recofremoving()
        newrec.dispo = object.dispo
        current_user = request.user
        newrec.deletedby = current_user.username
        newrec.save()
        object.delete()
        if searchedBy == 'dispo':
            searched = booklist.objects.all().filter(dispo__startswith=name)
        return render(request , 'editbooksection.html', {'searched':searched , 'name':name, 'searchedBy':searchedBy})
    except:
        messages.info(request, 'No more books')
        redirect('editbooksection')
def showrecofediting(request):
    return render(request, 'recofeditingform.html')
def showrecofdeleting(request):
    return render(request, 'recofremovingform.html')
def recofediting(request):
    if request.method == 'GET':
        details = []
        name = request.GET.get("searchedThis")
        details.append(name)
        for i in details:
            if i != "":
                searchedBy = request.GET.get("searchBy")
                if searchedBy == 'user':
                    searched = recordofediting.objects.all().filter(editedby__startswith=name)
                elif searchedBy == 'dispo':
                    searched = recordofediting.objects.all().filter(tdispo__startswith=name)   
                return render(request , 'recofediting.html', {'searched':searched, 'name':name, 'searchedBy':searchedBy})
            else:
                messages.info(request , 'What do you want me to make a record with ?')
                return redirect('showrecofediting')
def recofdeleting(request):
    if request.method == 'GET':
        details = []
        name = request.GET.get("searchedThis")
        details.append(name)
        for i in details:
            if i != "":
                searchedBy = request.GET.get("searchBy")
                if searchedBy == 'user':
                    searched = recofremoving.objects.all().filter(deletedby__startswith=name)
                elif searchedBy == 'dispo':
                    searched = recofremoving.objects.all().filter(dispo__startswith=name)   
                return render(request , 'recofremoving.html', {'searched':searched , 'name':name, 'searchedBy':searchedBy})
            else:
                messages.info(request , 'What do you want me to make a record with ?')
                return redirect('showrecofdeleting')
def changepic(request):
    if request.method == "POST":
            current_user = request.user
            name = current_user.username
            id = current_user.id
            profile = userprofile()
            u = User.objects.get(username=name)
            try:
                profile.profile_pic = request.FILES['image']
            except:
                messages.info(request , '*Upload a image please')
                return redirect('changepic')
            if userprofile.objects.filter(user=id).exists():
                prev = userprofile.objects.get(user=id)
                prev.delete()
                profile.user = u
            else:
                profile.user = u
            profile.save()
        
            #userprofile.save()
            return redirect("/")
        
            messages.info(request, "*Please, choose an image")
            return redirect("changepic")
    return render(request , 'imageupload.html')


def downloadbookrec(request ,name ,searchedBy):
    if searchedBy == 'bookdispo':
        searched = booktaken.objects.all().filter(bookdispo__startswith=name)        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bookrecord.csv"'

    writer = csv.writer(response)
    writer.writerow(['Book dispo','Name','number','Receiving time', 'Submission Time'])
    for search in searched:
        writer.writerow([search.bookdispo ,search.borrower.name, search.borrower.number ,search.taken_at , search.given_at ])
    return response
    
def downloadquery(request, name , searchedBy):
    if searchedBy == 'dispo':
        searched = booklist.objects.all().filter(dispo__startswith=name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="book_details.csv"'

    writer = csv.writer(response)
    writer.writerow(['Dispo', 'Taker or not'])
    for search in searched:
        if search.borrowed_book == True:
            writer.writerow([search.dispo ,'Borrowed' ])
        else:
            writer.writerow([search.dispo , 'Not Borrowed' ])
    return response
def downloadrecofediting(request, name , searchedBy):
    if searchedBy == 'user':
        searched = recordofediting.objects.all().filter(editedby__startswith=name)
    elif searchedBy == 'dispo':
        searched = recordofediting.objects.all().filter(dispo__startswith=name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Record_of_Editing.csv"'

    writer = csv.writer(response)
    writer.writerow(['Staff Name', 'Before/Then', 'Book Name'])
    for search in searched:
        writer.writerow([ search.editedby , 'Before' ,search.bdispo ])
        writer.writerow([ ' ' , 'After' ,search.tdispo ])
    return response
def downloadrecofdeleting(request, name , searchedBy):
    if searchedBy == 'user':
        searched = recofremoving.objects.all().filter(deletedby__startswith=name)
    elif searchedBy == 'dispo':
        searched = recofremoving.objects.all().filter(dispo__startswith=name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Record_of_Deleting.csv"'

    writer = csv.writer(response)
    writer.writerow(['Staff Name', 'Dispo'])
    for search in searched:
        writer.writerow([ search.deletedby ,search.dispo  ])
        
    return response

def editstaff(request):
    return render(request, 'editstaffform.html')
def editstaffform(request):
    if request.method == 'GET': 
        name = request.GET.get("searchedThis")
        if name == " ":
            messages.info(request , 'What do you want me to search with ?')
            return redirect("editstaff")
        else:
            searched = User.objects.all().filter(username__startswith=name)
            return render(request , 'editstafftable.html', {'searched':searched , 'name':name})
def editstaffsection(request , search_username , name):
    user = User.objects.get(username=search_username)
    if request.method == 'POST':
        id = user.id
        prev = permissions.objects.get(user=id)
        prev.delete()
        newuser = permissions()
        newuser.user = user
        if "addbook" in request.POST:
            newuser.addbook = True
        if "addstaff" in request.POST:
            newuser.addstaff = True
        if "editbooks" in request.POST:
            newuser.editbooks = True
        if "editstaff" in request.POST:
            newuser.editstaff = True
        if "recofredited" in request.POST:
            newuser.recofredited = True
        if "recofdeleted" in request.POST:
            newuser.recofdeleted = True
        if "removebook" in request.POST:
            newuser.removebook = True
        if "removestaff" in request.POST:
            newuser.removestaff = True
        newuser.save()
        searched = User.objects.all().filter(username__startswith=name)
        return render(request , 'editstafftable.html', {'searched':searched , 'name':name})

    
    return render(request , 'editstaffsection.html' ,{'user':user, 'search_username':search_username , 'name':name })