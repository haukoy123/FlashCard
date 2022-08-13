from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.forms import ProfileForm
from CardGroups.models import CardGroup
from Cards.models import Card
from datetime import datetime, time, timezone, timedelta



class SetUp(TestCase):
    client = Client()
    user_model = get_user_model()
    cardgroup_model = CardGroup
    card_model = Card

    cardgroup_data = {
        'name': 'test_cardgroup',
        'study_duration': timedelta(minutes=12),
        'last_study_at': datetime(2020, 12, 31, 20, 30),
        'study_count': 10
    }
    user_data = {
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test123456',
        'avatar': 'images/avatar_test.jpg'
    }
    card_data = {
        'front': 'hello',
        'back':'chào'
    }


    def create_user(self, data):
        if data is None:
            raise ValueError('data phải có dữ liệu')
        user = self.user_model()
        user.username = data.get('username')
        user.email = data.get('email')
        user.avatar = data.get('avatar')
        user.set_password(data.get('password'))
        user.save()
        return user



    def create_cardgroup(self, data, user):
        if data is None:
            raise ValueError('data phải có dữ liệu')
        cardgroup = self.cardgroup_model()
        cardgroup.user = user
        cardgroup.name = data.get('name')
        cardgroup.study_duration = data.get('study_duration')
        cardgroup.study_duration = data.get('study_duration')
        cardgroup.save()
        return cardgroup



    def create_card(self, data, cardgroup):
        if data is None:
            raise ValueError('data phải có dữ liệu')
        card = self.card_model()
        card.card_group = cardgroup
        card.front = data.get('front')
        card.back = data.get('back')
        card.save()
        return card



class LoginAndLogoutTestCase(SetUp):

    def setUp(self):
        self.user = self.create_user(data=self.user_data)


    def test_get_login_register_page(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login_register.html')


    def test_correct_login(self):
        response = self.client.post(reverse('users:login'), {'username': self.user_data.get('username'), 'password': self.user_data.get('password')})
        self.assertRedirects(response, reverse('cardgroups:learn'), 302, 200)


    def test_incorrect_login(self):
        # thiếu username/email
        response = self.client.post(reverse('users:login'), {'username': '', 'password': 'test123456'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['login_form'].is_valid())
        self.assertTrue(response.context['login_form'].has_error('username'))

        # sai username/email/password
        response = self.client.post(reverse('users:login'), {'username': 'no name', 'password': 'test123456'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['login_form'].is_valid())
        self.assertTrue(response.context['login_form'].has_error('__all__'))





class RegisterTestCase(SetUp):

    def setUp(self):
        self.user = self.create_user(data=self.user_data)


    def test_registration_successful(self):
        response = self.client.post(
            reverse('users:register'),
            {
                'username': 'test1',
                'password': 'test123456',
                'email': 'test1@gmail.com'
            }
        )
        user = get_user_model().objects.filter(username='test1')
        self.assertRedirects(response, reverse('cardgroups:learn'), 302, 200)
        self.assertEqual(1, len(user))
        self.assertTrue(user[0].check_password('test123456'))


    def test_registration_failed(self):
        response = self.client.post(
            reverse('users:register'),
            {
                'username': 'test',
                'password': 'test123456',
                'email': 'test'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['register_form'].is_valid())
        self.assertTrue(response.context['register_form'].has_error('email'))
        self.assertTrue( response.context['register_form'].has_error('username'))



class ProfileTestCase(SetUp):

    def setUp(self):
        user_2 = {
            'username': 'test_2',
            'email': 'test_2@gmail.com',
            'password': 'test_123456',
            'avatar': 'images/avatar_test_2.jpg'
        }
        user_1 = self.create_user(data=self.user_data)
        user_2 = self.create_user(data=user_2)

        self.response = self.client.login(username=self.user_data['username'], password=self.user_data['password'])


    def test_profile_get(self):
        self.assertTrue(self.response)
        response = self.client.get(path=reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertTrue(isinstance(response.context['form'], ProfileForm))


    def test_profile_update_successful(self):
        self.assertTrue(self.response)
        user = get_user_model().objects.get(username=self.user_data['username'])

        with open('static/public/images/flash_card.png', 'rb') as img:
            response = self.client.post(
                path=reverse('users:profile'),
                data={
                    'username': 'test_update',
                    'email': 'test_update@gmail.com',
                    'avatar': img
                }
            )
        self.assertRedirects(response, reverse('users:profile'), 302, 200)
        updated_user = get_user_model().objects.filter(username='test_update')
        self.assertEqual(1, len(updated_user))
        self.assertNotEqual(user, updated_user)


    def test_profile_update_failed(self):
        self.assertTrue(self.response)
        response = self.client.post(
            path=reverse('users:profile'),
            data={
                'username': 'test_2',
                'email': 'test_2@gmail.com'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].has_error('username'))
        self.assertTrue(response.context['form'].has_error('email'))


class PasswordChangeTestCase(SetUp):

    def setUp(self):
        user = self.create_user(data=self.user_data)
        self.response = self.client.login(username=self.user_data['username'], password=self.user_data['password'])

    def test_password_change_successful(self):
        self.assertTrue(self.response)
        response = self.client.post(reverse('users:password-change'), {
            'current_password': self.user_data['password'],
            'password': 'changed123456'
        })
        self.assertRedirects(response, reverse('cardgroups:learn'), 302, 200)
        user = get_user_model().objects.get(username='test')
        self.assertTrue(user.check_password('changed123456'))


    def test_password_change_failed(self):
        # nhập mật khẩu hiện tại sai
        self.assertTrue(self.response)
        response = self.client.post(reverse('users:password-change'), {
            'current_password': '123456789',
            'password': 'changed123456'
        })
        self.assertTrue(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].has_error('current_password'))

        # mật khẩu mới yếu
        response = self.client.post(reverse('users:password-change'), {'current_password': 'test123456', 'password': '123'})
        self.assertTrue(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].has_error('password'))
