from datetime import datetime, timedelta
import random
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
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
from dateutil import parser
from django.contrib import messages

from django.template import loader




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


    if request.method == 'GET':
        return redirect('cardgroups:group_details', pk)

    card_group = get_object_or_404(CardGroup, pk=pk, user=request.user)

    expire_date = set_expire_date(request, card_group)
    if expire_date is None:
        return redirect('cardgroups:group_details', pk)

    template_name = 'cardgroups/show_card_in_study_screen.html'
    html = get_html(
        request,
        template_name,
        {
            'card': request.session.get('card'),
            'cardgroup_pk': pk
        }
    )
    context = {
        'card': request.session.get('card'),
        'cardgroup': card_group,
        'expiredate': expire_date,
        'html': html
    }

    if check_session(request, pk):
        # expire_date = parser.parse(request.session.get('expire_date'))
        return render(request, 'cardgroups/study.html', context)
    # else:
        # expire_date = set_expire_date(request)

    update_card_group_last(card_group)
    cards = get_list_or_404(Card, card_group_id=pk, card_group__user=request.user)
    random.shuffle(cards)

    set_session_data(request, cards)
    index = index_of_selected_card(request)
    set_session_card(request, index)
    set_session_expire_date(request, expire_date)
    update_prority_level(request, index)

    html = get_html(
        request,
        template_name,
        {
            'card': request.session.get('card'),
            'cardgroup_pk': pk
        }
    )
    context['card'] = request.session.get('card')
    context['html'] = html

    return render(request, 'cardgroups/study.html', context)



def get_html(request, template_name, context):
    template = loader.get_template(template_name)
    return template.render(context, request)


def set_session_data(request, cards):
    max_priority_level = len(cards)
    data = list()
    for card in cards:
        data.append({'priority_level': max_priority_level, 'card':model_to_dict(card)})
        max_priority_level -= 1

    request.session['data'] = data


def set_session_card(request, index):
    data = request.session.get('data')
    card = data[index]['card'].copy()
    card.pop('back')
    start_time = timezone.now()

    request.session['card'] = {'index': index, 'card': card, 'start_time': str(start_time)}


def set_session_expire_date(request, expire_date):
    if isinstance(expire_date, datetime):
        request.session['expire_date'] = str(expire_date)
    else:
        request.session['expire_date'] = expire_date


def set_session_statistics(request, result=True):
    try:
        answered_correctly = request.session['statistics']['answered_correctly']
        answered_wrong = request.session['statistics']['answered_wrong']
    except KeyError:
        answered_correctly = 0
        answered_wrong = 0

    if result:
        answered_correctly += 1
    else:
         answered_wrong += 1

    statistics = {
        'answered_correctly': answered_correctly,
        'answered_wrong': answered_wrong
    }

    request.session['statistics'] = statistics


def update_card_group_last(card_group):
    card_group.last_study_at = timezone.now()
    study_count_last = card_group.study_count
    card_group.study_count = study_count_last + 1
    card_group.save()


def check_session(request, pk):
    # REVIEW 1: cần đặt tên hàm cụ thể hơn hoặc viết docstring
    # REVIEW 2: nên xuống dòng
    if request.session.get('data') and request.session.get('expire_date') and request.session.get('card') and request.session.get('card')['card']['card_group'] == pk:
        expire_date = parser.parse(request.session.get('expire_date'))
        if expire_date > timezone.now():
            return True
    return False


def set_expire_date(request, card_group):
    try:
        duration = int(request.POST['new_study_duration'])
    except KeyError:
        duration = card_group.study_duration
    except ValueError:
        messages.error(request, 'Thời gian ôn tập phải là số nguyên dương')
        return None

    if isinstance(duration, datetime):
        # REVIEW: phép cộng giữa datetime với datetime không thực hiện được
        return timezone.now() + duration
    return timezone.now() + timedelta(minutes=duration)


def update_prority_level(request, index, speed=None, result=None):
    data = request.session.get('data')
    if speed is None and result is None:
        data[index]['priority_level'] = data[index]['priority_level'] - len(data)
        for item in data:
            item['priority_level'] += 1
    else:
        if not result:
            if len(data) > 3:
                data[index]['priority_level'] += len(data) - 3
            else:
                data[index]['priority_level'] += 2
        else:
            if speed == 'normal':
                data[index]['priority_level'] += round(len(data) * 20 / 100)
            elif speed == 'slow':
                data[index]['priority_level'] += round(len(data) * 40 / 100)

    request.session['data'] = data


def index_of_selected_card(request):
    data = request.session.get('data')
    max_priority_level = max(data, key=lambda x: x['priority_level'])['priority_level']
    index_cards = [i for i in range(len(data)) if data[i]['priority_level'] == max_priority_level]
    if len(index_cards) > 1:
        index_card = random.choice(index_cards)
    else:
        index_card = index_cards[0]

    return index_card



@login_required()
def ContinueStudyingView(request, pk):
    if request.is_ajax():
        if check_session(request, pk):
            index = index_of_selected_card(request)
            set_session_card(request, index)
            update_prority_level(request, index)
            template_name = 'cardgroups/show_card_in_study_screen.html'
            html = get_html(request, template_name, {'card': request.session.get('card'), 'cardgroup_pk': pk})
            return JsonResponse({'card': request.session.get('card'), 'html': html}, status=200)
        else:
            return EndStudy(request, pk)
            # return JsonResponse({'expired': True, 'redirect': reverse('cardgroups:group_details', args=[pk])})
    return redirect('cardgroups:group_details', pk)




@login_required()
def CheckResult(request, pk):
    session_card = request.session.get('card')
    card = request.session.get('data')[session_card['index']]['card']
    answered_back = request.POST.get('back')
    back = card['back']

    time_start = parser.parse(session_card['start_time'])
    time_answered = timezone.now() - time_start

    result = False
    speed = None
    if answered_back.strip().casefold() == back.strip().casefold():
        result = True
        speed = check_time(card['back'].strip().casefold(), time_answered)
    
    set_session_statistics(request, result)

    update_prority_level(request, session_card['index'], speed, result)
    template_name = 'cardgroups/show_result_in_study_screen.html'
    html = get_html(request, template_name, {'result': result, 'card': card, 'cardgroup_pk': pk, 'answered_back': answered_back})

    return JsonResponse({'result': result, 'card': card, 'data': request.session.get('data'), 'html': html}, status=200)




def check_time(back, real_time):
    seconds_per_letter = 2
    typing_time = seconds_per_letter * len(back)
    thinking_time = real_time.seconds - typing_time

    if thinking_time < 3:
        return 'fast'
    if thinking_time > 6:
        return 'slow'
    else:
        return 'normal'



@login_required()
def EndStudy(request, pk):
    try:
        # REVIEW: nên code sao để nếu 1 key nào đó ko có trong request.session thì các key khác vẫn phải del thành công
        statistics = request.session['statistics']
        del request.session['card']
        del request.session['data']
        del request.session['statistics']
        del request.session['expire_date']
    except KeyError:
        return redirect('cardgroups:group_details', pk)

    if request.is_ajax():
        template_name = 'cardgroups/show_statistics_in_study_screen.html'
        html = get_html(request, template_name, statistics)
        return JsonResponse({'html': html})
    else:
        return redirect('cardgroups:group_details', pk)
