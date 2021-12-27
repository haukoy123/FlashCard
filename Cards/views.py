from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from Cards.models import Card
from Cards.forms import CardForm
from CardGroups.models import CardGroup
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.contrib import messages



@method_decorator(login_required, name='dispatch')
class CreateCard(generic.CreateView):
    model = Card
    form_class = CardForm
    template_name = 'cards/create_card.html'

    def get_initial(self):
        init = super().get_initial()
        init['card_group'] = self.kwargs.get('pk')
        return init

    def get(self, request, *args: str, **kwargs):
        if kwargs['btn'] == 'begin':
            return super().get(request, *args, **kwargs)
        else:
            return redirect('cards:create_card', self.kwargs['pk'], 'begin')

    def get_success_url(self):
        if self.kwargs['btn'] == 'continue':
            return reverse('cards:create_card', args=[self.kwargs['pk'], 'begin'])
        else:
            return reverse('cardgroups:group_details', args=[self.kwargs['pk']])


    def get_context_data(self, **kwargs):
        groups = CardGroup.objects.prefetch_related('cards').annotate(
                card_count=Count('cards__id'))
        group = get_object_or_404(groups, id=self.kwargs['pk'], user_id=self.request.user.pk)
       
        kwargs['group'] = group
        return super().get_context_data(**kwargs)




@login_required()
def DeleteCard(request, id_group, id_card):
    instance = get_object_or_404(Card, pk=id_card, card_group_id=id_group, card_group__user=request.user)
    if request.method == 'POST':
        instance.delete()
    return redirect('cardgroups:group_details', id_group)



@login_required()
def UpdateCard(request, id_group, id_card, page):
    instance = get_object_or_404(Card, pk=id_card, card_group_id=id_group, card_group__user=request.user)
    if request.method == 'POST':
        form = CardForm(instance=instance, data={**request.POST.dict(), 'card_group': id_group})
        if form.is_valid():
            form.save()
        else:
            messages.error(request, 'Cập nhật card thất bại')

    return redirect(reverse('cardgroups:group_details', args=[id_group]) + '?page=' + str(page))
