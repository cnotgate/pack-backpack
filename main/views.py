from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.forms import ItemForm
from main.models import Item
from django.http import HttpResponse
from django.core import serializers

# Create your views here.


# Fungsi ini digunakan untuk me-render main page '/' dengan
# data yang bersesuaian
def show_main(request):
    items = Item.objects.all()
    context = {
        'name': 'Ahmad Fatih Faizi',
        'class': 'PBP B',
        'items': items,
        'count': items.count()
    }

    return render(request, "main.html", context)


# Fungsi ini digunakan untuk me-render page add item yang akan
# digunakan user untuk menambahkan item baru.
def add_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "add_item.html", context)


def show_items_html(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, "items.html", context)


def show_items_xml(request):
    items = Item.objects.all()
    return HttpResponse(serializers.serialize("xml", items), content_type="application/xml")


def show_items_xml_by_id(request, id):
    item = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", item), content_type="application/xml")


def show_items_json_by_id(request, id):
    item = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", item), content_type="application/json")


def show_items_json(request):
    items = Item.objects.all()
    return HttpResponse(serializers.serialize("json", items), content_type="application/json")
