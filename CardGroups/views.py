from django.db.models.options import DEFAULT_NAMES
from django.shortcuts import redirect, render, render
from django.views import generic, View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from CardGroups.models import CardGroup
from django.utils.decorators import method_decorator
from django.db.models import Count
from CardGroups.forms import CardGroupForm
from django.urls import reverse_lazy
from django.urls import reverse



@method_decorator(login_required, name='dispatch')
class CardGroupView(generic.ListView):
    model = CardGroup
    template_name = 'cardgroups/dashboard.html'

    def get_queryset(self):
        return CardGroup.objects.prefetch_related('cards').annotate(
            card_count=Count('cards__id')
        ).filter(user_id=self.request.user.pk)
    


@method_decorator(login_required, name='dispatch')
class CreateGroup(generic.CreateView):
    model = CardGroup
    form_class = CardGroupForm
    template_name = 'cardgroups/create_group.html'

    def get_success_url(self):
        return reverse('cards:create_card', args=[self.object.pk, 'begin'])



@method_decorator(login_required, name='dispatch')
class GroupDetails(generic.DetailView):
    model = CardGroup
    template_name = 'cardgroups/group_details.html'

    def get_queryset(self):
        return CardGroup.objects.prefetch_related('cards').annotate(
            card_count=Count('cards__id')
        ).filter(user_id=self.request.user.pk)



@method_decorator(login_required, name='dispatch')
class DeleteGroup(generic.DeleteView):
    pass



@method_decorator(login_required, name='dispatch')
class UpdateGroup(generic.UpdateView):
    pass
