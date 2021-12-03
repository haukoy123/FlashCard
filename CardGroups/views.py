from functools import partial
from django.db.models.options import DEFAULT_NAMES
from django.shortcuts import get_list_or_404, redirect, render, render
from django.views import generic, View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from CardGroups.models import CardGroup
from Cards.models import Card
from django.utils.decorators import method_decorator
from django.db.models import Count
from CardGroups.forms import CardGroupForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger
from Cards.forms import CardForm




@method_decorator(login_required, name='dispatch')
class CardGroupView(generic.ListView):
    model = CardGroup
    template_name = 'cardgroups/dashboard.html'

    def get_queryset(self):
        queryset = CardGroup.objects.prefetch_related('cards').annotate(
            card_count=Count('cards__id')
        ).filter(user_id=self.request.user.pk)

        if self.request.GET.get('group'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('group'))
        return queryset
    


@method_decorator(login_required, name='dispatch')
class CreateGroup(generic.CreateView):
    model = CardGroup
    form_class = CardGroupForm
    template_name = 'cardgroups/create_group.html'


    def get_success_url(self):
        return reverse('cards:create_card', args=[self.object.pk, 'begin'])


    def get_initial(self):
        init = super().get_initial()
        init['user'] = self.request.user.pk
        return init



# @method_decorator(login_required, name='dispatch')
# class GroupDetails(generic.DetailView):
#     model = CardGroup
#     template_name = 'cardgroups/group_details.html'

#     def get_queryset(self):
#         return CardGroup.objects.prefetch_related('cards').annotate(
#             card_count=Count('cards__id')
#         ).filter(user_id=self.request.user.pk)



@method_decorator(login_required, name='dispatch')
class DeleteGroup(generic.DeleteView):
    model = CardGroup
    success_url = reverse_lazy('cardgroups:learn')



@method_decorator(login_required, name='dispatch')
class UpdateGroup(generic.UpdateView):
    model = CardGroup   
    form_class = CardGroupForm
    template_name = 'cardgroups/group_details.html'


    def get_cards(self):
        return get_list_or_404(Card, card_group_id=self.kwargs['pk'])


    def get_card_paginator(self):
        return Paginator(self.get_cards(), 2)


    def get_card_page(self):
        card_paginator = self.get_card_paginator()
        if self.request.GET.get('page'):
            page_number = int(self.request.GET.get('page'))
            if page_number >=1 and page_number <= card_paginator.num_pages:
                return card_paginator.get_page(page_number)

        return card_paginator.get_page(1)


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['cardgroup'] = CardGroup.objects.prefetch_related('cards').annotate(
            card_count=Count('cards__id')
        ).filter(user_id=self.request.user.pk, id=self.kwargs['pk'])[0]
        context_data['card_page'] = self.get_card_page()
        card = self.get_card_page().object_list[0]
        # thẻ input của study_duration trong html có kiểu "number" và nhận vào đơn vị là phút
        # mà trong initial: study_duration dạng timedelta ->form của study_duration nhận values: vd '00:10:02'-> k hiển thị được 

        study_duration_seconds = context_data['form'].initial['study_duration'].seconds
        study_duration_minutes = round(study_duration_seconds/60, 2)
        context_data['form'].initial['study_duration'] = study_duration_minutes
        context_data['card_form'] = CardForm(instance=card)
        return context_data

    

@login_required()
def GroupDetails(request):
    pass
    