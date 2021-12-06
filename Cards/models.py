from CardGroups.models import CardGroup
from django.db import models


class Card(models.Model):
    card_group = models.ForeignKey(CardGroup, on_delete=models.CASCADE, related_name='cards')
    front = models.TextField()
    back = models.TextField()

    def __str__(self):
        return self.front


    class Meta:
        db_table = "card"
        ordering = ["id"]
