import users
from Cards.forms import CardForm
from django.test import TestCase
from Cards.models import Card
from CardGroups.tests import CardGroupSetUp
from django.urls import reverse




class CardSetUp(CardGroupSetUp):
    card_model = Card

    card_data = {
        'front': 'hello',
        'back':'chào'
    }

    def create_card(self, data, cardgroup):
        if data is None:
            raise ValueError('data phải có dữ liệu')
        card = self.card_model()
        card.card_group = cardgroup
        card.front = data.get('front')
        card.back = data.get('back')
        card.save()
        return card


class CardTestCase(CardSetUp):

    def setUp(self):
        self.user = self.create_user(data=self.user_data)
        self.cardgroup = self.create_cardgroup(data=self.cardgroup_data, user=self.user)
        self.card = self.create_card(data=self.card_data, cardgroup=self.cardgroup)
        self.response = self.client.login(username=self.user_data['username'], password=self.user_data['password'])


    def test_get_create_card_page(self):
        response = self.client.get(reverse('cards:create_card', args=[self.cardgroup.pk, 'begin']))
        self.assertTemplateUsed(response, 'cards/create_card.html')
        self.assertTrue(isinstance(response.context['form'], CardForm))


    def test_create_card_successful(self):

    # tạo card ở trang tạo card
    # mục đích: tiếp tục tạo card mới
        response = self.client.post(
            path=reverse('cards:create_card', args=[self.cardgroup.pk, 'continue']),
            data = {'front': 'white', 'back': 'trắng'}
        )
        cards = self.card_model.objects.all()
        self.assertRedirects(response, reverse('cards:create_card', args=[self.cardgroup.pk, 'begin']), 302, 200)
        self.assertEqual(cards.count(), 2)

    # tạo card chuyển về trang chi tiết chồng card
    # mục đích: không muốn thêm card mới
        response = self.client.post(
            path=reverse('cards:create_card', args=[self.cardgroup.pk, 'done']),
            data = {'front': 'red', 'back': 'đỏ'}
        )
        cards = self.card_model.objects.all()
        self.assertRedirects(response, reverse('cardgroups:group_details', args=[self.cardgroup.pk]), 302, 200)
        self.assertEqual(cards.count(), 3)


    def test_create_card_failed(self):
        response = self.client.post(
            path=reverse('cards:create_card', args=[self.cardgroup.pk, 'continue']),
            data = {'front': '', 'back': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].has_error('front'))
        self.assertTrue( response.context['form'].has_error('back'))


    def test_update_card_successful(self):
        data = {
            'front': 'test_update_card',
            'back': 'chào'
        }
        response = self.client.post(
            path=reverse('cards:update_card', args=[self.cardgroup.pk, self.card.pk, 1]),
            data = data
        )
        self.assertRedirects(response, reverse('cardgroups:group_details', args=[self.cardgroup.pk]) + '?page=' + str(1), 302, 200)
        card = self.card_model.objects.get(pk=self.card.pk)
        self.assertEqual(card.front, data['front'])



    def test_update_card_failed(self):
        front_before_update = self.card.front
        back_before_update = self.card.back
        response = self.client.post(
            path=reverse('cards:update_card', args=[self.cardgroup.pk, self.card.pk, 1]),
            data = {'front': '', 'back': ''}
        )
        card = self.card_model.objects.get(pk=self.card.pk)
        self.assertEqual(card.front, front_before_update)
        self.assertEqual(card.back, back_before_update)


    def test_delete_card(self):
        cardgroup_pk = self.cardgroup.pk
        card_pk = self.card.pk
        response = self.client.post(
            path=reverse('cards:delete_card', args=[cardgroup_pk, card_pk])
        )

        card = self.card_model.objects.filter(pk=card_pk)
        self.assertEqual(0, card.count())
        self.assertRedirects(response, reverse('cardgroups:group_details', args=[cardgroup_pk]), 302, 200)
