from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Quote
from ..login_and_registration_app.models import User
# import datetime
# Create your views here.
def index(request):
    # User.objects.all().delete()
    # Quotes.objects.all().delete()
    return render(request, 'quotes_app/index.html')

def quotes(request):
    # print "*"*42
    if not request.session.get('id'):
        messages.error(request, 'Access Denied. Log in first.')
        return redirect('/')
    user = User.objects.get(id=request.session.get('id'))
    print user
    quotables = Quote.objects.all().exclude(faves=user)
    favorites = Quote.objects.filter(faves=user)
    context = {
        'user': user,
        'quotables': quotables,
        'favorites': favorites,
    }
    # print context
    return render(request, 'quotes_app/quotes.html', context)

def add_to_faves(request):
    if not request.session.get('id'):
        messages.error(request, 'Access Denied. Log in first.')
        return redirect('/')
    if request.method == 'POST':
        # print request.POST
        # print request.POST['appt_id']
        quote = Quote.objects.get(id=request.POST['quote'])
        user = User.objects.get(id=request.session.get('id'))
        quote.faves.add(user)
        quote.save()
    return redirect('/quotes')


def add_a_quote(request):
    if not request.session.get('id'):
        messages.error(request, 'Access Denied. Log in first.')
        return redirect('/')
    results = Quote.objects.addQuoteVal(request.POST)
    if not results['error_message'] == []:
        for error in results['error_message']:
            messages.error(request, error)
    else:
        messages.success(request, 'Quote Successfuly Added.')
        # return redirect('books/'+str(results['book'].id))
    return redirect('/quotes')

def remove_fave(request):
    if not request.session.get('id'):
        messages.error(request, 'Access Denied. Log in first.')
        return redirect('/')
    if request.method == 'POST':
        quote = Quote.objects.get(id=request.POST['fave'])
        user = User.objects.get(id=request.session.get('id'))
        quote.faves.remove(user)
        quote.save()
    return redirect('/quotes')

def user_page(request, id):
    user = User.objects.get(id=id)
    quotes_by_user = Quote.objects.filter(posted_by=user)
    quote_count = quotes_by_user.count()
    # print "*"*42
    # print quote_count
    # print "*"*42
    # print quotes_by_user
    # print appt_time_str
    context = {
        'user' : user,
        'quotes_by_user' : quotes_by_user,
        'quote_count' : quote_count
    }
    # print context
    return render(request, 'quotes_app/user_page.html', context)

def logout(request):
    request.session.clear()
    messages.success(request, 'Logged Out')
    return redirect('/')

def home(request):
    return redirect('/quotes')
