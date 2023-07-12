from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from fitness_users.models import FitnessUser
from .constants import UserRoleChoice
from .models import DietRecord

sample_diet_record = {
    'fitness_user_id': 1,
    'diet_date': '2023-07-01',
    'diet_time': '12:00:00',
    'diet_description': 'Sample diet description',
    'approximate_calorie': 500
}


class DietRecordCreateTests(APITestCase):
    def setUp(self):
        self.user = FitnessUser.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.url = reverse('diet-records-add')

    def test_create_diet_record(self):
        data = {**sample_diet_record, 'fitness_user_id': self.user.id}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DietRecord.objects.count(), 1)
        self.assertEqual(DietRecord.objects.get().fitness_user_id, self.user.id)

    def test_create_diet_record_for_other_user(self):
        other_user = FitnessUser.objects.create_user(username='otheruser', password='test_password')
        data = {**sample_diet_record, 'fitness_user_id': other_user.id}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DietRecord.objects.count(), 0)

    def test_create_diet_record_unauthenticated(self):
        self.client.logout()
        data = {**sample_diet_record, 'fitness_user_id': self.user.id}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DietRecord.objects.count(), 0)


class DietRecordRWDTests(APITestCase):
    def setUp(self):
        self.user = FitnessUser.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.diet_record = DietRecord.objects.create(
            fitness_user_id=self.user.id,
            diet_date=sample_diet_record['diet_date'],
            diet_time=sample_diet_record['diet_time'],
            diet_description=sample_diet_record['diet_date'],
            approximate_calorie=500
        )
        self.url = reverse('diet-records-info', args=[self.diet_record.pk])

    def test_get_diet_record(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.diet_record.pk)

    def test_update_diet_record(self):
        data = {
            'diet_date': '2023-07-02',
            'diet_time': '13:00:00',
            'diet_description': 'Updated diet description',
            'approximate_calorie': 600
        }
        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['diet_date'], '2023-07-02')
        self.assertEqual(response.data['diet_time'], '13:00:00')
        self.assertEqual(response.data['diet_description'], 'Updated diet description')
        self.assertEqual(response.data['approximate_calorie'], 600)

    def test_delete_diet_record(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DietRecord.objects.filter(pk=self.diet_record.pk).exists())


class DietRecordListTests(APITestCase):
    def setUp(self):
        self.admin_user = FitnessUser.objects.create_user(username='admin', password='adminpassword', is_staff=True)
        self.manager_user = FitnessUser.objects.create_user(username='manager', password='managerpassword', role=UserRoleChoice.MANAGER)
        self.client.login(username='admin', password='adminpassword')
        self.diet_record = DietRecord.objects.create(
            fitness_user_id=self.manager_user.id,
            diet_date=sample_diet_record['diet_date'],
            diet_time=sample_diet_record['diet_time'],
            diet_description=sample_diet_record['diet_date'],
            approximate_calorie=500
        )
        self.url = reverse('diet-records')

    def test_list_diet_records_as_admin(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.diet_record.pk)

    def test_list_diet_records_as_manager(self):
        self.client.login(username='manager', password='managerpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.diet_record.pk)

    def test_list_diet_records_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserDietRecordListTests(APITestCase):
    def setUp(self):
        self.user = FitnessUser.objects.create_user(username='test_user', password='test_password')
        self.manager = FitnessUser.objects.create_user(username='manageruser', password='test_password', role=UserRoleChoice.MANAGER)
        self.client.login(username='test_user', password='test_password')
        self.diet_record_1 = DietRecord.objects.create(
            fitness_user_id=self.user.id,
            diet_date='2023-07-01',
            diet_time='12:00:00',
            diet_description='Sample diet description 1',
            approximate_calorie=500
        )
        self.diet_record_2 = DietRecord.objects.create(
            fitness_user_id=self.user.id,
            diet_date='2023-07-02',
            diet_time='13:00:00',
            diet_description='Sample diet description 2',
            approximate_calorie=600
        )
        self.url = reverse('diet-user-records', kwargs={'user_id': self.user.id})

    def test_get_user_diet_records_as_owner(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.diet_record_1.pk)
        self.assertEqual(response.data[1]['id'], self.diet_record_2.pk)

    def test_get_user_diet_records_as_manager(self):
        self.client.login(username='manageruser', password='test_password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.diet_record_1.pk)
        self.assertEqual(response.data[1]['id'], self.diet_record_2.pk)

    def test_get_user_diet_records_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_diet_records_invalid_user_id(self):
        invalid_url = reverse('diet-user-records', kwargs={'user_id': 999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_diet_records_forbidden(self):
        user2 = FitnessUser.objects.create_user(username='user2', password='test_password')
        invalid_url = reverse('diet-user-records', kwargs={'user_id': user2.id})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DietRecordModelTests(TestCase):
    def setUp(self):
        self.user = FitnessUser.objects.create_user(username='test_user', password='test_password')
        self.diet_record = DietRecord.objects.create(
            fitness_user_id=self.user.id,
            diet_date=sample_diet_record['diet_date'],
            diet_time=sample_diet_record['diet_time'],
            diet_description=sample_diet_record['diet_date'],
            approximate_calorie=500
        )

    def test_diet_record_str(self):
        expected_str = f"{self.user.id} | 2023-07-01 | 12:00:00 | 500"
        self.assertEqual(str(self.diet_record), expected_str)
