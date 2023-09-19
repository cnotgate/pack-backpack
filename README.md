# Pack's Backpack

---

# Tugas 2

- [x] Membuat input form untuk menambahkan objek model pada app sebelumnya.
- [x] Tambahkan 5 fungsi views untuk melihat objek yang sudah ditambahkan dalam format HTML, XML, JSON, XML by ID, dan JSON by ID.
- [x] Membuat routing URL untuk masing-masing views yang telah ditambahkan pada poin 2.
- [x] Menjawab beberapa pertanyaan berikut pada README.md pada root folder.
  - [X] Apa perbedaan antara form POST dan form GET dalam Django?
  - [X] Apa perbedaan utama antara XML, JSON, dan HTML dalam konteks pengiriman data?
  - [X] Mengapa JSON sering digunakan dalam pertukaran data antara aplikasi web modern?
  - [X] Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
- [X] Mengakses kelima URL di poin 2 menggunakan Postman, membuat screenshot dari hasil akses URL pada Postman, dan menambahkannya ke dalam README.md.
- [X] Melakukan add-commit-push ke GitHub.

## Pengimplementasian Checklist

### Prerequisites
  
- Membuat folder `templates` pada rot folder.
- Membuat file `base.html` pada folder `templates` yang berisi
  
  ```HTML
  {% load static %}
  <!DOCTYPE html>
  <html lang="en">
      <head>
          <meta charset="UTF-8" />
          <meta
              name="viewport"
              content="width=device-width, initial-scale=1.0"
          />
          {% block meta %}
          {% endblock meta %}
      </head>

      <body>
          {% block content %}
          {% endblock content %}
      </body>
  </html>
  ```

- Mendaftarkan template yang baru saja dibuat pada `pack_backpack/settings.py` pada variabel `TEMPLATES`

  ```python
  ...
  TEMPLATES = [
      {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [BASE_DIR / 'templates'], # Tambahkan kode ini
          'APP_DIRS': True,
          ...
      }
  ]
  ...
  ```

- Mengubah `main/templates/main.html` menjadi:

  ```html
  {% extends 'base.html' %}

  {% block content %}
  <h1>Pack's Backpack</h1>

  <h4>Name: {{name}}</h4>

  <h4>Class: {{class}}</h4>

  {% include 'items.html' %}

  <br>

  <a href="{% url 'main:add_item' %}">
    <button>
      Add New Item to Backpack
    </button>
  </a>

  {% endblock content %}
  ```

  >Perhatikan bahwa kita menggunakan `{% include 'items.html' %}` untuk memuat isi dari `items.html` ke file `main.html` untuk mengurangi code redundancy, karena content yang ditampilkan sama.

### Membuat input form

- Membuat file baru pada direktori `main` dengan nama `forms.py` yang diisi dengan kode berikut:

    ```python
    from django.forms import ModelForm
    from main.models import Item

    class ItemForm(ModelForm):
      class Meta:
          model = Item
          fields = ["name", "amount", "rarity", "description"]
    ```

    >Kode ini merupakan struktur dari form yang akan kita gunakan untuk menerima input data dari user.

    >`model` adalah model data yang akan kita gunakan pada form (Pada kasus ini adalah `Item`).

    >`fields` adalah isian apa saja yang akan ditampilkan di forms. Pada kasus ini, isian yang akan ditampilkan adalah name, amount, rarity, dan description.

  - Menambahkan beberapa import pada `main/views.py`

    ```python
    from django.http import HttpResponseRedirect
    from main.forms import ItemForm
    from django.urls import reverse
    ```
  
  - Membuat fungsi baru pada file yang sama dengan nama `add_item`

    ```python
    def add_item(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "add_item.html", context)
    ```

    >Fungsi ini berguna untuk menampilkan page form.

  - Membuat file HTML baru dengan nama `add_item.html` pada `main/templates` yang berisi:

    ```html
    {% extends 'base.html' %} 

    {% block content %}
    <h1>Add New Item</h1>

    <form method="POST">
        {% csrf_token %}
        <table>
            {{ form.as_table }}
            <tr>
                <td></td>
                <td>
                    <input type="submit" value="Add Item"/>
                </td>
            </tr>
        </table>
    </form>

    {% endblock %}
    ```

### Menambahkan 5 fungsi views untuk melihat objek yang sudah ditambahkan dalam format HTML, XML, JSON, XML by ID, dan JSON by ID
  
- Menambahkan beberapa import pada file `main/views.py`.

  ```python
  from main.models import Item
  from django.http import HttpResponse
  from django.core import serializers
  ```

- Menambahkan fungsi baru pada `main/views.py` yang bernama `show_items_html` yang berisi:

  ```python
  def show_items_html(request):
      items = Item.objects.all()
      context = {'items': items}

      return render(request, "items.html", context)
  ```

- Menambahkan file HTML baru bernama `items.html` pada `main/templates` yang berisi:

  ```html
  {% extends 'base.html' %}

  {% block content %}

  <table>
    <tr>
      <th>Name</th>
      <th>Amount</th>
      <th>Rarity</th>
      <th>Description</th>
    </tr>

    {% for item in items %}
    <tr>
      <td>{{item.name}}</td>
      <td>{{item.amount}}</td>
      <td class="{{item.rarity}}">{{item.rarity}}</td>
      <td>{{item.description}}</td>
    </tr>
    {% endfor %}
  </table>

  <style>
    table,
    th,
    td {
      border: 1px solid black;
      border-collapse: collapse;
      text-align: center;
      table-layout: fixed;
    }

    td {
      width: 10em;
    }

    .Common {
      color: gray;
    }

    .Uncommon {
      color: green;
    }

    .Rare {
      color: blue;
    }

    .VeryRare {
      color: violet;
    }

    .Epic {
      color: orange;
    }

    .Legendary {
      color: orangered;
    }
  </style>

  {% endblock content %}
  ```

  >Di sini saya menambahkan styling menggunakan CSS untuk mempercantik tampilan web.

- Menambahkan kode berikut pada `main/views.py`

  ```python
  ...
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

  def show_items_json(request):
      items = Item.objects.all()
      return HttpResponse(serializers.serialize("json", items), content_type="application/json")

  def show_items_json_by_id(request, id):
      item = Item.objects.filter(pk=id)
      return HttpResponse(serializers.serialize("json", item), content_type="application/json")
  ...
  ```

  > Perhatikan bahwa pada fungsi `show_items_xml_by_id` dan `show_items_json_by_id` kita menggunakan method `filter` untuk melakukan pencarian item dengan `id` yang sesuai.

### Routing URL

- Meng-import fungsi-fungsi yang sudah kita buat di `main/views.py` pada `main/urls.py`

  ```python
  from main.views import show_main, add_item, show_items_html, show_items_xml, show_items_json, show_items_xml_by_id, show_items_json_by_id
  ```

- Menambahkan kode berikut pada `main/urls.py` pada `urlpatterns`
  
  ```python
  ...
  path('add-item/', add_item, name='add_item'),
  path('html/', show_items_html, name='show_items_html'),
  path('xml/', show_items_xml, name='show_items_xml'),
  path('json/', show_items_json, name='show_items_json'),
  path('xml/<int:id>/', show_items_xml_by_id, name='show_items_xml_by_id'),
  path('json/<int:id>/', show_items_json_by_id, name='show_items_json_by_id'),
  ...
  ```

### Pengerjaan poin BONUS

- Menambahkan kode berikut pada `main/views.py` pada `context` di fungsi `show_main`

```python
...
'count': items.count()
...
```

- Menambahkan kode berikut pada `main/templates/main.html`

```html
...
<h4>Item(s) in your backpack: {{count}}</h4>
...
```

## Perbedaan antara form GET dan form POST dalam Django

Perbedaan yang paling terlihat antara GET dan POST adalah, GET menyematkan data yang akan disubmit ke dalam URL, sedangkan POST tidak, POST akan menyematkan data yang akan disubmit pada HTTP message body.

## Perbedaan utama antara XML, JSON, dan HTML dalam konteks pengiriman data

Pada dasarnya ketiga format tersebut bisa digunakan untuk transmisi data, tetapi terdapat perbedaan fundamental pada ketiga format tersebut.

HTML digunakan untuk tranmisi data yang akan digunakan untuk tampilan web, sedangkan XML dan JSON adalah format yang digunakan untuk transmisi data.

XML menggunakan sintaks yang kurang lebih sama seperti HTML. XML menggunakan nested tag untuk mendefinisikan hirarki. Kita bisa menambahkan comment di XML

JSON menggunakan sintaks seperti object javascript (key value pair). JSON menggunakan nested object untuk mendefinisikan hirarki. Kita tidak bisa menambahkan comment pada JSON.

## Mengapa JSON sering digunakan dalam pertukaran data antara aplikasi web modern?
Karena JSON di-support oleh banyak bahasa dan framework, ringan, dan human readable. JSON terintegrasi dengan Javascript (Bahasa yang populer digunakan untuk web development). JSON secara performa parsing juga lebih cepat jika dibandingkan dengan XML.

## Screenshot Postman

### HTML

![Alt text](./docs/assets/postmanhtml.png)

### XML

![Alt text](./docs/assets/postmanxml.png)

### JSON

![Alt text](./docs/assets/postmanjson.png)

### XML by id

![Alt text](./docs/assets/postmanxmlid.png)

### JSON by id

![Alt text](./docs/assets/postmanjsonid.png)

---

# Tugas 1

- [x] Membuat sebuah proyek Django baru.
- [x] Membuat aplikasi dengan nama main pada proyek tersebut.
- [x] Melakukan routing pada proyek agar dapat menjalankan aplikasi main.
- [x] Membuat model pada aplikasi main dengan nama Item dan memiliki atribut wajib sebagai berikut.
- name sebagai nama item dengan tipe CharField.
- amount sebagai jumlah item dengan tipe IntegerField.
- description sebagai deskripsi item dengan tipe TextField.
- [x] Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML yang menampilkan nama aplikasi serta nama dan kelas kamu.
- [x] Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py.
- [x] Melakukan deployment ke Adaptable terhadap aplikasi yang sudah dibuat sehingga nantinya dapat diakses oleh teman-temanmu melalui Internet.
- [x] Membuat sebuah README.md yang berisi tautan menuju aplikasi Adaptable yang sudah di-deploy, serta jawaban dari beberapa pertanyaan berikut.
- Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
- Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.
- Jelaskan mengapa kita menggunakan virtual environment? Apakah kita tetap dapat membuat aplikasi web berbasis Django tanpa menggunakan virtual environment?
- Jelaskan apakah itu MVC, MVT, MVVM dan perbedaan dari ketiganya.

## Pengimplementasian Checklist

- ### Membuat proyek Django baru

  - Membuat direktori `pack_backpack`
  - Membuat virtual environment
  - Membuat & mengaktifkan virtual environment
  - Menginstall Django dan beberapa dependencies
  - Menjalankan command `django-admin startproject pack_backpack`
  - Menambahkan "*" pada `ALLOWED_HOSTS` di `settings.py`

- ### Membuat aplikasi `main` pada proyek `pack_backpack`
  
  - Menjalankan command `python manage.py startapp main` untuk membuat aplikasi `main`
  - Mendaftarkan aplikasi `main` pada proyek dengan menambahkannya di variabel `INSTALLED_APPS` pada `/pack_backpack/settings.py`
  - Membuat direktori `templates` untuk memuat semua template yang akan digunakan pada aplikasi
  - Membuat `main.html` di dalam direktori `templates` yang isinya sebagai berikut:

    ```html
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Pack's Backpack</title>
      </head>
      <body>
        <h1>Pack's Backpack</h1>
        <p>Nama: {{ name }}</p>
        <p>Kelas: {{ class }}</p>
      </body>
    </html>
    ```

    Perhatikan bahwa `name` dan `class` merupakan variabel yang akan kita definisikan di `views.py`

  - Mendefinisikan `name` dan `class` pada `views.py`
  
  ```python
  ...
  def show_main(request):
    context = {
        'name': 'Ahmad Fatih Faizi',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)
  ...
  ```

- ### Melakukan routing

  - buat file `urls.py` baru di dalam direktori `main` yang berisi:

  ```python
  from django.urls import path
  from main.views import show_main

  app_name = 'main'

  urlpatterns = [
      path('', show_main, name='show_main'),
  ]
  ```

  Perhatikan bahwa di sini kita memetakan route "/" kepada fungsi `show_main` yang terdapat di `views.py`. Sehingga ketika user mengakses route "/", variabel-variabel yang telah didefinisikan pada fungsi `show_main` akan di-render.

  - Import `include` ke `urls.py` pada direktori proyek
  
  ```python
  ...
  from django.urls import include
  ...
  ```
  
  - Menambahkan route pada variabel `urlpatterns` di `urls.py`

  ```python
  urlpatterns = [
    ...
    path('', include('main.urls')),
    ...
  ]
  ```

  Di sini kita memetakan route "/" kepada `urls.py` pada `main`. Sehingga ketika user mengakses route "/", route yang telah didefinisikan di `urls.py` pada `main` akan berjalan.

  Perhatikan juga bahwa route `urls.py` pada `main` akan relatif terhadap route yang didefinisikan pada `urls.py` proyek.

- ### Deployment

  - Membuat app baru di Adaptable
  - Menghubungkan repository `pack_backpack` ke Adaptable
  - Deploy aplikasi

## Bagan Struktur & Cara Kerja Django

```mermaid
flowchart TD
  A[User request\nhttps://pack-backpack.adaptable.io] --> B[urls.py]
  B -- Memetakan route '/' kepada\nviews yang bersangkutan --> C[views.py]
  C -- meng-update data --> D[models.py]
  D -- mengambil data context\n untuk dirender --> C
  C -- render data yang\ndidapatkan dari models  --> E[main.html]
  E -- input dari user --> C
```

## Mengapa menggunakan virtual environment?

Virtual environment berguna jika kita mempunyai banyak proyek python yang memiliki dependencies dengan versi yang berbeda-beda. Dengan menggunakan virtual environment, kita bisa "mengisolasi" satu versi dari suatu dependency tanpa memengaruhi dependency yang sama pada proyek lain, sehingga semua proyek tetap bisa dijalankan walaupun dependency-nya memiliki versi yang berbeda-beda.

Kita bisa saja membuat proyek Django tanpa menggunakan virtual environment, tetapi jika kita memiliki beberapa proyek dengan dependency yang sama, maka dependency tersebut harus memiliki versi yang sama.

## MVT, MVC, MVVM

MVT, MVC, dan MVVM merupakan beberapa dari banyak software arcitecture pattern. Architecture pattern membuat codebase mudah di-maintain dengan menerapkan aturan-aturan baku dalam struktur kode, dan menerapkan "separation of concerns".

### MVT (Model View Template)

- Model

  Komponen yang menyimpan dan me-maintain data pada aplikasi.

- View

  Merupakan komponen yang menjadi antarmuka pengguna (UI)

- Template

  Merupakan komponen static yang menjadi dasar dari View untuk ditambahkan data-data dinamis.

### MVC (Model View Controller)

- Model

  Merupakan komponen yang menyimpan data.

- View

  Merupakan komponen yang menjadi antarmuka pengguna (UI)
  
- Controller

  Komponen yang mengontrol data flow dari Model dan View

### MVVM (Model View Viewmodel)

- Model

    Komponen yang me-maintain data bersama dengan Viewmodel

- View

    Merupakan komponen yang menjadi antarmuka pengguna (UI)

- Viewmodel

    Komponen yang mengontrol data flow dari Model dan View. Viewmodel meneruskan data-data yang akan dirender kepada View
