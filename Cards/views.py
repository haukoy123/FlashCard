from django.http.response import Http404
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from Cards.models import Card
from Cards.forms import CardForm
from CardGroups.models import CardGroup
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



@method_decorator(login_required, name='dispatch')
class CreateCard(generic.CreateView):
    model = Card
    form_class = CardForm
    template_name = 'cards/create_card.html'

    def get(self, request, *args: str, **kwargs):
        if kwargs['btn'] == 'begin':
            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse('cards:create_card', args=[self.kwargs['pk'], 'begin']))

    def get_success_url(self):
        if self.kwargs['btn'] == 'continue':
            return reverse('cards:create_card', args=[self.kwargs['pk'], 'begin'])
        else:
            return reverse('cardgroups:learn')

    def get_context_data(self, **kwargs):
        try:
            group = CardGroup.objects.get(id=self.kwargs['pk'], user_id=self.request.user.pk)
        except CardGroup.DoesNotExist as e:
            raise Http404("Không tìm thấy chồng card nào")
        kwargs['group'] = group
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return super().get_context_data(**kwargs)



@method_decorator(login_required, name='dispatch')
class CardDetails(generic.DetailView):
    pass