from django.http.response import Http404
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from Cards.models import Card
from Cards.forms import CardForm
from CardGroups.models import CardGroup
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count



@method_decorator(login_required, name='dispatch')
class CreateCard(generic.CreateView):
    model = Card
    form_class = CardForm
    template_name = 'cards/create_card.html'

    def get(self, request, *args: str, **kwargs):
        if kwargs['btn'] == 'begin':
            return super().get(request, *args, **kwargs)
        else:
            return redirect('cards:create_card', self.kwargs['pk'], 'begin')

    def get_success_url(self):
        if self.kwargs['btn'] == 'continue':
            return reverse('cards:create_card', args=[self.kwargs['pk'], 'begin'])
        else:
            return reverse('cardgroups:group_details')

    def get_context_data(self, **kwargs):
        # group = get_object_or_404(CardGroup, id=self.kwargs['pk'], user_id=self.request.user.pk)

        # REVIEW:
        # 1) Khi viết ".filter(...)[0]" thì sẽ không xảy ra lỗi CardGroup.DoesNotExist, mà là lỗi IndexError
        # viết ".filter(...).get()", hoặc ".get(...)" thì mới là lỗi CardGroup.DoesNotExist
        # 2) Em có thể dùng hàm get_object_or_404, nó nhận biến đầu tiên là model hoặc queryset
        try:
            group = CardGroup.objects.prefetch_related('cards').annotate(
                card_count=Count('cards__id')
            ).filter(id=self.kwargs['pk'], user_id=self.request.user.pk)[0]
        except CardGroup.DoesNotExist as e:
            raise Http404("Không tìm thấy chồng card nào")

        kwargs['group'] = group
        return super().get_context_data(**kwargs)



@method_decorator(login_required, name='dispatch')
class CardDetails(generic.DetailView):
    pass


@login_required()
def DeleteCard(request, id_group, id_card):
    # REVIEW: cần thêm điều kiện, "card_group__user=request.user". Vì sao?
    instance = get_object_or_404(Card, pk=id_card, card_group_id=id_group)
    if request.method == 'POST':
        instance.delete()
    return redirect('cardgroups:group_details', id_group)



@login_required()
def UpdateCard(request, id_group, id_card):
    # REVIEW: cần thêm điều kiện, "card_group__user=request.user". Vì sao?
    instance = get_object_or_404(Card, pk=id_card, card_group_id=id_group)
    if request.method == 'POST':
        form = CardForm(instance=instance, data={**request.POST.dict(), 'card_group': id_group})
        if form.is_valid():
            form.save()
    return redirect('cardgroups:group_details', id_group)
