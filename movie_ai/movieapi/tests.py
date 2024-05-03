from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

class MovieAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_short_form_1(self):
        response = self.client.post('/short_form/', {"query": "Scenes of the Wizard."}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_short_form_2(self):
        response = self.client.post('/short_form/', {"query": "Scene where the Witch melts."}, format='json')
        resp_timestamp = response.json()["timestamp"]
        oracle_timestampe = {"start":"02:39","end":"03:12"}
        self.assertEqual(resp_timestamp, oracle_timestampe)

    def test_video_qa_1(self):
        response = self.client.post('/video_qa/', {"query":"How did the witch die?"}), format='json'
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_video_qa_2(self):
        response = self.client.post('/video_qa/', {"query":"What did the Wizard tell Dorothy to do?"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_avatar_chat_1(self):
        response = self.client.post('/avatar_chat/', {"query": "What did it feel like to encounter the Wizard?", "Character": "Dorothy"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_avatar_chat_2(self):
        response = self.client.post('/avatar_chat/', {"query": "How did melting feel like?", "Character": "Witch"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

