import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.forms import ItemForm
from main.models import Item
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# Fungsi ini digunakan untuk me-render main page dengan
# data yang bersesuaian
@login_required(login_url='/login')
def show_main(request):
    items = Item.objects.filter(user=request.user)
    try:
        context = {
            'name': request.user.username,
            'class': 'PBP B',
            'items': items,
            'count': items.count(),
            'last_login': request.COOKIES['last_login'],
        }
    except KeyError:
        date = datetime.datetime.now()
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(
            date.strftime("%d %B, %Y, %H:%M")))
        context = {
            'name': request.user.username,
            'class': 'PBP B',
            'items': items,
            'count': items.count(),
            'last_login': request.COOKIES['last_login'],
        }

    return render(request, "main.html", context)


# Fungsi ini digunakan untuk me-render page add item yang akan
# digunakan user untuk menambahkan item baru.
def add_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "add_item.html", context)


@csrf_exempt
def add_item_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        rarity = request.POST.get("rarity")
        description = request.POST.get("description")
        user = request.user
        newItem = Item(name=name, amount=amount, rarity=rarity,
                       description=description, user=user)
        newItem.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()


def show_items_html(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, "items.html", context)


def show_items_xml(request):
    items = Item.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", items), content_type="application/xml")


def show_items_xml_by_id(request, id):
    item = Item.objects.filter(pk=id, user=request.user)
    return HttpResponse(serializers.serialize("xml", item), content_type="application/xml")


def show_items_json_by_id(request, id):
    item = Item.objects.filter(pk=id, user=request.user)
    return HttpResponse(serializers.serialize("json", item), content_type="application/json")


def show_items_json(request):
    items = Item.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", items), content_type="application/json")


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            date = datetime.datetime.now()
            response.set_cookie('last_login', str(
                date.strftime("%d %B, %Y, %H:%M")))
            return response
        else:
            messages.info(
                request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def increment(request, id):
    items = Item.objects.filter(user=request.user)
    item = Item.objects.get(pk=id)
    if item in items:
        item.amount = item.amount+1
        item.save()
        return redirect('main:show_main')


def decrement(request, id):
    items = Item.objects.filter(user=request.user)
    item = Item.objects.get(pk=id)
    if item in items:
        if (item.amount == 1):
            item.delete()
        else:
            item.amount = item.amount - 1
        item.save()
        return redirect('main:show_main')


def delete(request, id):
    items = Item.objects.filter(user=request.user)
    item = Item.objects.get(pk=id)
    if item in items:
        item = Item.objects.filter(pk=id)
        item.delete()
        return redirect('main:show_main')
