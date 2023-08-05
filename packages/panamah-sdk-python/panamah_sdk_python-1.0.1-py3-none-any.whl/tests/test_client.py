from unittest import main, mock, TestCase
from panamah_sdk.client import AdminClient, StreamClient
from .server import start as start_test_server, stop as stop_test_server, set_next_response, clear_next_response


class TestClient(TestCase):
    @classmethod
    def setUpClass(cls):
        start_test_server()

    @classmethod
    def tearDownClass(cls):
        stop_test_server()

    def tearDown(self):
        clear_next_response()

    def test_admin_client(self):
        """testing admin client"""
        client = AdminClient("auth")
        # get
        set_next_response(200, {'id': 1})
        response = client.get("/admin/assinantes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.content, 'utf-8'), '{"id": 1}')
        # post
        set_next_response(201, {'id': 1})
        response = client.post("/admin/assinantes", {'id': 1})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(str(response.content, 'utf-8'), '{"id": 1}')

    def test_stream_client(self):
        """testing stream client"""
        client = StreamClient("auth", "secret")
        with mock.patch.object(client, 'authenticate') as authenticate_method:
            authenticate_method.return_value = {
                'accessToken': '123',
                'refreshToken': 'refresh_12983123',
            }
            response = client.post("/stream/data", {"s": 1})
            authenticate_method.assert_called_once_with('auth', 'secret', '*')
            self.assertEqual(response.status_code, 200)
            with mock.patch.object(client, 'refresh_tokens') as refresh_method:
                refresh_method.return_value = {
                    'accessToken': 'a501925913',
                    'refreshToken': 'b284422321',
                }
                set_next_response(403, {})
                response = client.post("/stream/data", {"s": 1})
                clear_next_response()
                refresh_method.assert_called_once_with('refresh_12983123')

    def test_stream_client_key_calculation(self):
        """testing stream client key calc"""
        client = StreamClient("auth", "secret")
        self.assertEqual(client.calculate_key('123', '*', 1563551838), 'ZRx/dmsZhQzbm+zqIE/ML6Bq6uo=')

if __name__ == '__main__':
    main()
