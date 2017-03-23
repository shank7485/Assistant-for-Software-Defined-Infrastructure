import unittest

import base


class TestEndPoint(base.TestBase):
    def setUp(self):
        super(TestEndPoint, self).setUp()

    def test_index_page_status(self):
        """ send HTTP GET request to the application on the index page. """
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page_status(self):
        """ send HTTP GET request to the application on the login page. """
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_logout_page_status(self):
        """ send HTTP GET request to the application on the logout page
            to check whether it redirects the request to the login page. """
        response = self.client.get('/logout', content_type='html/text')
        self.assertEqual(response.status_code, 302)

    def test_chat_page_status(self):
        """ send HTTP GET request to the application on the chat page
            with a msg/question to get a response from the bot. """
        response = self.client.get('/chat?question=Hi',
                                   content_type='html/text')
        self.assertEqual(response.status_code, 302)

    def test_set_endpoint_status(self):
        """ send HTTP GET request to the application on the set page. """
        response = self.client.get('/set',
                                   content_type='html/text')
        self.assertEqual(response.status_code, 302)
        self.assertIn('Redirecting', response.data)

    def test_consoleScreen_endpoint_status(self):
        """ send HTTP GET request to the application on the consoleScreen page. """
        response = self.client.get('/consoleScreen',
                                   content_type='html/text')
        self.assertEqual(response.status_code, 302)
        self.assertIn('Redirecting', response.data)

    def test_getConsoleLog_endpoint_status(self):
        """ send HTTP GET request to the application on the getConsoleLog page. """
        response = self.client.get('/getConsoleLog',
                                   content_type='html/text')
        self.assertEqual(response.status_code, 302)
        self.assertIn('Redirecting', response.data)

    # TODO(ndahiwade): Add other endpoints in the App to check if the
    # endpoints are working fine

if __name__ == '__main__':
    unittest.main()
