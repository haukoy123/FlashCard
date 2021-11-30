from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse



class CardGroup(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='cardGroups')
    name = models.CharField(max_length=50)
    study_duration =models.DurationField(null=True, blank=True)
    last_study_at =  models.DateTimeField(_('last study'), blank=True, null=True)
    study_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


    # def get_absolute_url(self):
    #     reverse('cardgroups:group_details', args=[self.pk])




    class Meta:
        db_table = "cardgroup"
        ordering = ["-study_count", 'id']