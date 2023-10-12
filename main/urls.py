from django.urls import path
from main.views import show_main, add_item, show_items_html, show_items_xml, show_items_json, show_items_xml_by_id, show_items_json_by_id, register, login_user, logout_user, delete, increment, decrement, add_item_ajax

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add-item/', add_item, name='add_item'),
    path('html/', show_items_html, name='show_items_html'),
    path('xml/', show_items_xml, name='show_items_xml'),
    path('json/', show_items_json, name='show_items_json'),
    path('xml/<int:id>/', show_items_xml_by_id, name='show_items_xml_by_id'),
    path('json/<int:id>/', show_items_json_by_id, name='show_items_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('delete/<int:id>/', delete, name='delete'),
    path('increment/<int:id>/', increment, name='increment'),
    path('decrement/<int:id>/', decrement, name='decrement'),
    path('create-ajax/', add_item_ajax, name='add_item_ajax'),
]
