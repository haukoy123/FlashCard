from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from users.tests import SetUp
from CardGroups.forms import CardGroupForm
from dateutil import parser
from django.shortcuts import get_list_or_404
from django.forms.models import model_to_dict
from freezegun import freeze_time


class CardGroupTestCase(SetUp):

    def setUp(self):
        self.user = self.create_user(data=self.user_data)
        self.cardgroup = self.create_cardgroup(data=self.cardgroup_data, user=self.user)
        self.response = self.client.login(username=self.user_data['username'], password=self.user_data['password'])


    def test_get_cardgroup_list(self):
        response = self.client.get(path=reverse('cardgroups:learn'))
        self.assertTemplateUsed(response, 'cardgroups/dashboard.html')
        self.assertNotEqual(len(response.context['cardgroup_list']), 0)


    def test_get_cardgroup_details(self):
        response = self.client.get(path=reverse('cardgroups:group_details', args=[self.cardgroup.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cardgroups/group_details.html')
        self.assertIsInstance(response.context['form'], CardGroupForm)


    def test_create_cardgroup_successful(self):
        data = {
            'name':'test_create_cardgroup',
            'study_duration': 10
        }
        response = self.client.post(
            path=reverse('cardgroups:create_group'),
            data = data
        )
        cardgroup = self.cardgroup_model.objects.filter(name=data['name'])
        self.assertEqual(len(cardgroup), 1)
        self.assertRedirects(response, reverse('cards:create_card', args=[cardgroup[0].pk, 'begin']), 302, 200)


    def test_create_cardgroup_failed(self):
        data = {
            'name':'',
            'study_duration': 'sgdj'
        }

        response = self.client.post(
            path=reverse('cardgroups:create_group'),
            data = data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].has_error('name'))
        self.assertTrue( response.context['form'].has_error('study_duration'))


    def test_update_cardgroup_successful(self):
        data = {
            'name':'test_update_cardgroup',
            'study_duration': 10
        }
        response = self.client.post(
            path=reverse('cardgroups:group_details', args=[self.cardgroup.pk]),
            data = data
        )

        self.assertRedirects(response, reverse('cardgroups:group_details', args=[self.cardgroup.pk]), 302, 200)
        cardgroup = self.cardgroup_model.objects.get(pk=self.cardgroup.pk)
        self.assertEqual(cardgroup.name, data['name'])


    def test_update_cardgroup_failed(self):
        data = {
            'name':'test_update_cardgroup',
            'study_duration': 'jkjfbhd'
        }
        response = self.client.post(
            path=reverse('cardgroups:group_details', args=[self.cardgroup.pk]),
            data = data
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue( response.context['form'].has_error('study_duration'))


    def test_delete_cardgroup(self):
        cardgroup_pk = self.cardgroup.pk
        response = self.client.post(
            path=reverse('cardgroups:delete_group', args=[cardgroup_pk])
        )
        cardgroup = self.cardgroup_model.objects.filter(pk=cardgroup_pk)
        self.assertEqual(0, cardgroup.count())
        self.assertRedirects(response, reverse('cardgroups:learn'), 302, 200)


class StudyTestCase(SetUp):

    def setUp(self):
        self.user = self.create_user(data=self.user_data)
        self.cardgroup = self.create_cardgroup(data=self.cardgroup_data, user=self.user)
        self.card = self.create_card(data=self.card_data, cardgroup=self.cardgroup)
        self.card_2 = self.create_card(data={'front': 'red', 'back': 'đỏ'}, cardgroup=self.cardgroup)
        self.response = self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        # session = self.client.session
        # session['study_type'] = 'front'
        # session['statistics'] = {
        #     'answered_correctly': 0,
        #     'answered_wrong': 0
        # }
        # session['expire_date'] = str(timezone.now() + timedelta(minutes=10))
        # session['data'] = [{'priority_level': 1, 'card': model_to_dict(self.card)}, {'priority_level': 2, 'card': model_to_dict(self.card_2)}]
        # card = model_to_dict(self.card).copy()
        # card.pop('back')
        # session['card'] = {'index': 0, 'card': card, 'start_time': str(timezone.now() - timedelta(seconds=10))}
        # session['expire_date'] = str(timezone.now() + timedelta(minutes=10))
        # session.save()


    @freeze_time('2021-01-01 03:21:34')
    def test_use_get_method_to_show_card_for_study(self):
        response = self.client.get(
            path=reverse('cardgroups:study_group', args=[self.cardgroup.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cardgroups/study.html')
        self.assertTemplateUsed(response, 'cardgroups/show_card_in_study_screen.html')
        session = self.client.session
        cards = self.card_model.objects.all()
        self.assertEqual(len(session['data']), cards.count())
        self.assertEqual(session['study_type'], 'shuffle')
        self.assertEqual(
            parser.parse(session['expire_date']),
            timezone.now() + self.cardgroup.study_duration
        )
        self.assertEqual(session['card'], response.context['card'])
        

    @freeze_time('2021-01-01 03:21:34')
    def test_use_post_method_to_show_card_for_study(self):
        study_duration = 10
        response = self.client.post(
            path=reverse('cardgroups:study_group', args=[self.cardgroup.pk]),
            data={'new_study_duration': study_duration, 'study_type': 'front'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cardgroups/study.html')
        self.assertTemplateUsed(response, 'cardgroups/show_card_in_study_screen.html')
        session = self.client.session
        cards = self.card_model.objects.all()     
        self.assertEqual(len(session['data']), cards.count())
        self.assertTrue(session.get('card'))
        self.assertTrue(session.get('expire_date'))
        self.assertEqual(session['study_type'], 'front')
        self.assertEqual(
            parser.parse(session['expire_date']),
            timezone.now() + timedelta(minutes=study_duration)
        )
        self.assertEqual(session['card'], response.context['card'])

    

    def test_check_result(self):
        response = self.client.post(
            path=reverse('cardgroups:study_group', args=[self.cardgroup.pk]),
            data={'new_study_duration': 10, 'study_type': 'front'}
        )
        session = self.client.session
        index_card = session.get('card')['index']
        card = session.get('data')[index_card]['card']

        response = self.client.post(
            path=reverse('cardgroups:check_result', args=[self.cardgroup.pk]),
            data={'back': card['back']}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cardgroups/show_result_in_study_screen.html')
        session = self.client.session
        self.assertTrue(response.context['result'])
        self.assertEqual(session['statistics']['answered_correctly'], 1)
        self.assertEqual(session['statistics']['answered_wrong'], 0)


    @freeze_time('2021-01-01 03:21:34')
    def test_show_next_card(self):    
        response = self.client.post(
            path=reverse('cardgroups:study_group', args=[self.cardgroup.pk]),
            data={'new_study_duration': 10, 'study_type': 'front'}
        )
        session = self.client.session
        index_card = session.get('card')['index']
        card = session.get('data')[index_card]['card']

        # trả lời cho card hiển thị đầu tiên (trả lời đúng)
        response = self.client.post(
            path=reverse('cardgroups:check_result', args=[self.cardgroup.pk]),
            data={'back': card['back']}
        )

        # lấy card thứ 2
        response = self.client.get(
            path=reverse('cardgroups:continues_studying', args=[self.cardgroup.pk]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cardgroups/show_card_in_study_screen.html')
        session = self.client.session
        self.assertEqual(session['card'], response.context['card'])

        session = self.client.session
        index_card = session.get('card')['index']
        card = session.get('data')[index_card]['card']

        # trả lời cho card thứ 2 (trả lời sai)
        response = self.client.post(
            path=reverse('cardgroups:check_result', args=[self.cardgroup.pk]),
            data={'back': card['back'] + '_wrong'}
        )

        # gọi card tiếp thì bị hết thời gian học
        session = self.client.session
        session['expire_date'] = str(timezone.now())
        session.save()
        response = self.client.get(
            path=reverse('cardgroups:continues_studying', args=[self.cardgroup.pk]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cardgroups/show_statistics_in_study_screen.html')
        session = self.client.session

        self.assertFalse(session.get('card'))
        self.assertFalse(session.get('expire_date'))
        self.assertFalse(session.get('data'))
        self.assertFalse(session.get('statistics'))
        self.assertFalse(session.get('study_type'))

        # vì trả lời 1 lần đúng và 1 lần sai ---> answered_correctly = 1, answered_wrong = 1
        self.assertEqual(response.context['answered_correctly'], 1)
        self.assertEqual(response.context['answered_wrong'], 1)

    def test_end_study(self):
        response = self.client.get(
            path=reverse('cardgroups:end_study', args=[self.cardgroup.pk]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        session = self.client.session
        self.assertFalse(session.get('card'))
        self.assertFalse(session.get('expire_date'))
        self.assertFalse(session.get('data'))
        self.assertFalse(session.get('statistics'))
        self.assertFalse(session.get('study_type'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cardgroups/show_statistics_in_study_screen.html')
