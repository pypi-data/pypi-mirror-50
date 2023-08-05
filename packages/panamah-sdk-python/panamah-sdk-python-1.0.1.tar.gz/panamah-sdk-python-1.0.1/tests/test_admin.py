import json
from unittest import main, mock, TestCase
from panamah_sdk.admin import PanamahAdmin
from panamah_sdk.models.base import Model, StringField
from panamah_sdk.models.definitions import PanamahAssinante
from .server import start as start_test_server, stop as stop_test_server, set_next_response, clear_next_response, get_last_request


class TestAdmin(TestCase):
    @classmethod
    def setUpClass(cls):
        start_test_server()

    @classmethod
    def tearDownClass(cls):
        stop_test_server()

    def tearDown(self):
        clear_next_response()

    def test_get_assinante(self):
        admin = PanamahAdmin('auth')
        set_next_response(200, {
            "id": "b4705ade-d0cf-4397-b38d-902aaebeb00c",
            "nome": "ASSINANTE TESTE",
            "fantasia": "ASSINANTE TESTE",
            "bairro": "VILA ISABEL CAFETEIRA",
            "cidade": "SÃO LUÍS",
            "ramo": "N/A",
            "uf": "MA",
            "ativo": True,
            "softwaresAtivos": [],
            "softwaresEmContratosDeManutencao": [],
            "planoUso": {}
        })
        assinante = admin.get_assinante('b4705ade-d0cf-4397-b38d-902aaebeb00c')
        self.assertTrue(isinstance(assinante, PanamahAssinante))
        self.assertEqual(assinante.id, 'b4705ade-d0cf-4397-b38d-902aaebeb00c')
        self.assertEqual(assinante.nome, 'ASSINANTE TESTE')
        self.assertEqual(assinante.fantasia, 'ASSINANTE TESTE')
        self.assertEqual(assinante.bairro, 'VILA ISABEL CAFETEIRA')
        self.assertEqual(assinante.cidade, 'SÃO LUÍS')
        self.assertEqual(assinante.ramo, 'N/A')
        self.assertEqual(assinante.uf, 'MA')
        self.assertEqual(assinante.ativo, True)

        set_next_response(404, {})
        try:
            admin.get_assinante('121')
        except Exception as e:
            self.assertEqual(str(e), 'Assinante nao existe.')

        set_next_response(500, {})
        try:
            admin.get_assinante('121')
        except Exception as e:
            self.assertEqual(str(e), 'Erro 500 ao tentar buscar um assinante.')

    def test_create_assinante(self):
        admin = PanamahAdmin('auth')
        assinante = PanamahAssinante(
            id="b4705ade-d0cf-4397-b38d-902aaebeb00c",
            nome="ASSINANTE TESTE",
            fantasia="ASSINANTE TESTE",
            bairro="VILA ISABEL CAFETEIRA",
            cidade="SÃO LUÍS",
            ramo="N/A",
            uf="MA",
            ativo=True
        )
        set_next_response(201, {
            "id": "b4705ade-d0cf-4397-b38d-902aaebeb00c",
            "nome": "ASSINANTE TESTE",
            "fantasia": "ASSINANTE TESTE",
            "bairro": "VILA ISABEL CAFETEIRA",
            "cidade": "SÃO LUÍS",
            "ramo": "N/A",
            "uf": "MA",
            "ativo": True
        })
        response = admin.create_assinante(assinante)

        last_request = get_last_request()

        self.assertDictEqual(last_request['payload'], {
            "id": "b4705ade-d0cf-4397-b38d-902aaebeb00c",
            "nome": "ASSINANTE TESTE",
            "fantasia": "ASSINANTE TESTE",
            "bairro": "VILA ISABEL CAFETEIRA",
            "cidade": "SÃO LUÍS",
            "ramo": "N/A",
            "uf": "MA",
            "ativo": True
        })

        self.assertEqual(response.id, 'b4705ade-d0cf-4397-b38d-902aaebeb00c')
        self.assertEqual(response.nome, 'ASSINANTE TESTE')
        self.assertEqual(response.fantasia, 'ASSINANTE TESTE')
        self.assertEqual(response.bairro, 'VILA ISABEL CAFETEIRA')
        self.assertEqual(response.cidade, 'SÃO LUÍS')
        self.assertEqual(response.ramo, 'N/A')
        self.assertEqual(response.uf, 'MA')
        self.assertEqual(response.ativo, True)

        set_next_response(409, {})
        try:
            admin.create_assinante(response)
        except Exception as e:
            self.assertEqual(str(e), 'Assinante ja existe.')

        set_next_response(500, {})
        try:
            admin.create_assinante(response)
        except Exception as e:
            self.assertEqual(str(e), 'Erro 500 ao criar um assinante.')

    def test_delete_assinante(self):
        admin = PanamahAdmin('auth')
        set_next_response(200, {})
        response = admin.delete_assinante(
            'b4705ade-d0cf-4397-b38d-902aaebeb00c')
        self.assertTrue(response)

        set_next_response(404, {})
        try:
            admin.delete_assinante('121')
        except Exception as e:
            self.assertEqual(str(e), 'Assinante nao existe.')

        set_next_response(500, {})
        try:
            admin.delete_assinante('121')
        except Exception as e:
            self.assertEqual(str(e), 'Erro 500 ao deletar um assinante.')


if __name__ == '__main__':
    main()
