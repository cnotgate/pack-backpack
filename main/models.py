from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    RARITIES = [
        ("Common", "Common"),
        ("Uncommon", "Uncommon"),
        ("Rare", "Rare"),
        ("Very rare", "Very rare"),
        ("Epic", "Epic"),
        ("Legendary", "Legendary")
    ]
    name = models.CharField(max_length=255)
    amount = models.IntegerField(default=1)
    rarity = models.CharField(max_length=9, choices=RARITIES)
    description = models.TextField(default='-')
