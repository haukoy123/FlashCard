import random
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render, render
from django.views import generic
from django.contrib.auth.decorators import login_required
from CardGroups.models import CardGroup
from Cards.models import Card
from django.utils.decorators import method_decorator
from django.db.models import Count
from CardGroups.forms import CardGroupForm
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from Cards.forms import CardForm
from django.utils import timezone
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http.response import Http404
from dateutil import parser



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
        cards = self.group.cards.all()
        return cards


    def get_card_paginator(self):

        return Paginator(self.get_cards(), 2)


    def get_card_page(self):
        card_paginator = self.get_card_paginator()
        if self.request.GET.get('page'):
            try:
                page_number = int(self.request.GET.get('page'))
            except ValueError:
                return card_paginator.get_page(1)

            if page_number >=1 and page_number <= card_paginator.num_pages:
                return card_paginator.get_page(page_number)
        return card_paginator.get_page(1)


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        queryset = CardGroup.objects.prefetch_related('cards').annotate(
            card_count=Count('cards__id')
        )
        self.group = get_object_or_404(queryset, user_id=self.request.user.pk, id=self.kwargs['pk'])
        context_data['cardgroup'] = self.group
        context_data['cards_page'] = self.get_card_page()
        cards = context_data['cards_page'].object_list
        context_data['cards_forms'] = [CardForm(instance=card) for card in cards]
        return context_data


@login_required()
def StudyView(request, pk):
    cards = get_list_or_404(Card,card_group_id=pk, card_group__user=request.user)
    random.shuffle(cards)
    max_priority_level = len(cards)
    data = list()
    for card in cards:
        data.append({'priority_level': max_priority_level, 'card':model_to_dict(card)})
        max_priority_level -= 1
        
    request.session['data'] = data

    # group = get_object_or_404(CardGroup, pk=pk)
    # if group.user == request.user:
    #     group.last_study_at = timezone.now()
    #     study_count_last = group.study_count
    #     group.study_count = study_count_last + 1
    #     group.save()
    # else:
    #     raise Http404('không tìm thấy group')

    index = index_of_selected_card(request)
    UpdatePriorityLevel(request, index)
    return render(request, 'cardgroups/study.html', {'card': request.session.get('card'), 'card_group': cards[index].card_group} )
    




def UpdatePriorityLevel(request, index):
    data = request.session.get('data')
    data[index]['priority_level'] = data[index]['priority_level'] - len(data)
    for item in data:
        item['priority_level'] = item['priority_level'] + 1

    request.session['data'] = data



def index_of_selected_card(request):
    data = request.session.get('data')
    max_priority_level = max(data, key=lambda x: x['priority_level'])['priority_level']
    index_cards = [i for i in range(len(data)) if data[i]['priority_level'] == max_priority_level]
    if len(index_cards) > 1:
        index_card = random.choice(index_cards)
    else:
        index_card = index_cards[0]
        
    card = data[index_card]['card'].copy()
    card.pop('back')
    start_time = timezone.now()
    request.session['card'] = {'index': index_card, 'card': card, 'start_time': str(start_time)}
    return index_card




def ContinueStudyingView(request, pk):
    if request.is_ajax():
        index = index_of_selected_card(request)
        UpdatePriorityLevel(request, index)
        # return render(request, 'cardgroups/study.html', {'card': context} )
        return JsonResponse({'card': request.session.get('card')}, status=200)

    return redirect('cardgroups:learn')



def CheckResult(request, pk):
    session_card = request.session.get('card')
    card = request.session.get('data')[session_card['index']]['card']
    back = request.GET.get('back')
    time_start = parser.parse(session_card['start_time'])
    time_answered = timezone.now() - time_start
    print(time_answered)

    result = False
    if back.casefold() == card['back'].casefold():
        result = True
    return JsonResponse({'result': result, 'card': card}, status=200)
