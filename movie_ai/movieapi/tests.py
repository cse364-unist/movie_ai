from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class MovieAPITestCase(APITestCase):

    def test_short_form_1(self):
        response = self.client.post(reverse('short_form'), {"query": "Scenes of the Wizard."})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_short_form_2(self):
        response = self.client.post(reverse('short_form'), {"query": "Scene where the Witch melts."})
        resp_timestamp = response.json()["timestamp"]
        oracle_timestampe = {"start":"02:39","end":"03:12"}
        self.assertEqual(resp_timestamp, oracle_timestampe)

    def test_short_form_3(self):
        response = self.client.post(reverse('short_form'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_video_qa_1(self):
        response = self.client.post(reverse('video_qa'), {"query":"How did the witch die?"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_video_qa_2(self):
        response = self.client.post(reverse('video_qa'), {"query":"What did the Wizard tell Dorothy to do?"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_video_qa_3(self):
        response = self.client.post(reverse('video_qa'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_avatar_chat_1(self):
        response = self.client.post(reverse('avatar_chat'), {"query": "What did it feel like to encounter the Wizard?", "character": "Dorothy"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_avatar_chat_2(self):
        response = self.client.post(reverse('avatar_chat'), {"query": "How did melting feel like?", "character": "Witch"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_avatar_chat_3(self):
        response = self.client.post(reverse('avatar_chat'), {"character": "Witch"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
