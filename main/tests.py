from django.test import TestCase, Client
from main.models import Item


class mainTest(TestCase):

    def test_main_url_is_exist(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('/')
        self.assertTemplateUsed(response, 'main.html')

    # Cek apakah aplikasi me-render views
    def test_main_rendering_views(self):
        response = Client().get('/')
        self.assertContains(response, "<p>Nama: Ahmad Fatih Faizi</p>")
        self.assertContains(response, "<p>Kelas: PBP B</p>")

    # Instantiate Item, lalu test instance Item tersebut
    def test_item(self):
        item = Item.objects.create(name="Wooden sword",
                                   amount=45,
                                   rarity="Common",
                                   description="A default sword for noobs")
        self.assertTrue(isinstance(item, Item))
        self.assertEqual(item.name, "Wooden sword")
        self.assertEqual(item.amount, 45)
        self.assertEqual(item.rarity, "Common")
        self.assertEqual(item.description, "A default sword for noobs")

    # Tes apakah default amount dari item adalah 1 jika argumen amount tidak di-supply
    def test_item_default_amount(self):
        item = Item.objects.create(name="Wooden sword",
                                   rarity="Common",
                                   description="A default sword for noobs")
        self.assertEqual(item.amount, 1)
