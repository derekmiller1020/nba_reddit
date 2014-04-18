from django.test import TestCase


class RetrieveThreadsTest(TestCase):

    def test_threads(self):

        resp = self.client.get('/threads/')

        #the basics
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('game_threads' in resp.context)


class RetrieveCommentsTest(TestCase):

    def test_comments(self):

        resp = self.client.get('/comments/?id=231hk5')

        #test the basics
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.context)
        self.assertTrue('can_comment' in resp.context)
        self.assertTrue('link' in resp.context)
        self.assertTrue('threads' in resp.context)

        #based on get request
        self.assertEqual(resp.context['threads'], '231hk5')

        #test that the user is not logged in
        self.assertEqual(resp.context['username'], '')
        self.assertEqual(resp.context['can_comment'], '')