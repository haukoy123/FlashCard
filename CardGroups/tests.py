from django.test import TestCase
from django.urls import reverse
from users.tests import SetUp
from CardGroups.forms import CardGroupForm
from dateutil import parser


class CardGroupTestCase(SetUp):

    def setUp(self):
        self.user = self.create_user(data=self.user_data)
        self.cardgroup = self.create_cardgroup(data=self.cardgroup_data, user=self.user)
        self.response = self.client.login(username=self.user_data['username'], password=self.user_data['password'])


    def test_get_cardgroup_list(self):
        response = self.client.get(path=reverse('cardgroups:learn'))
        self.assertTemplateUsed(response, 'cardgroups/dashboard.html')
        self.assertNotEqual(response.context['cardgroup_list'].count(), 0)


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
        self.assertEqual(cardgroup.count(), 1)
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
        self.response = self.client.login(username=self.user_data['username'], password=self.user_data['password'])


    def test_show_card_for_study(self):
    # sử dụng method GET
        response = self.client.get(
            path=reverse('cardgroups:study_group', args=[self.cardgroup.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cardgroups/study.html')
        self.assertTemplateUsed(response, 'cardgroups/show_card_in_study_screen.html')
        session = self.client.session
        cards = self.card_model.objects.all()
        self.assertEqual(len(session['data']), cards.count())

    # sử dụng method POST
        response = self.client.post(
            path=reverse('cardgroups:study_group', args=[self.cardgroup.pk]),
            data={'new_study_duration': 10}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cardgroups/study.html')
        self.assertTemplateUsed(response, 'cardgroups/show_card_in_study_screen.html')
        session = self.client.session
        cards = self.card_model.objects.all()     
        self.assertEqual(len(session['data']), cards.count())
        self.assertTrue(session.get('card'))
        self.assertTrue(session.get('expire_date'))
    
