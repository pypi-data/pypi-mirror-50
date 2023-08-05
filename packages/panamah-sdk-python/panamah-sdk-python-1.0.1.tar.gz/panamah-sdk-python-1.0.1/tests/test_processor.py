import os
import shutil
import json
from time import sleep
from unittest import main, mock, TestCase
from panamah_sdk.batch import Batch
from panamah_sdk.operation import Update
from panamah_sdk.processor import BatchProcessor, BATCH_MAX_LENGTH, BATCH_MAX_SIZE, BATCH_MAX_AGE, ROOT_PATH, ACCUMULATED_PATH, SENT_PATH
from panamah_sdk.models.base import Model, StringField
from panamah_sdk.models.definitions import PanamahHolding, PanamahAcesso, PanamahSecao, PanamahLoja, PanamahProduto
from .server import start as start_test_server, stop as stop_test_server, set_next_response, clear_next_response, get_last_request


class Response():
    def __init__(self, status_code, json_response):
        self.status_code = status_code
        self.json_response = json_response

    def json(self):
        return self.json_response


def test_expiration(self, by_max_length=False, by_max_size=False, by_max_age=False):
    holding = PanamahHolding(id='1234', descricao='teste')
    acesso = PanamahAcesso(id='4321', funcionario_ids=['1', '2'])
    secao = PanamahSecao(id='5555', codigo='6666', descricao='teste')

    b = BatchProcessor('auth', 'secret', '12345', batch_max_length=1 if by_max_length else 999999,
                       batch_max_size=80 if by_max_size else 99999 * 1024, batch_max_age=.5 if by_max_age else 9999999999)

    with mock.patch.object(b, 'send_accumulated_batches') as send_accumulated_batches_method:

        self.assertFalse(b.current_batch_expired())

        b.save(secao)

        if (by_max_age):
            sleep(.6)

        self.assertTrue(b.current_batch_expired())
        self.assertFalse(b.accumulated_batch_exists())
        batch_name = b.current_batch.get_filename_by_created_date()

        b.process()

        self.assertTrue(b.accumulated_batch_exists())
        self.assertTrue(os.path.exists('%s/%s' %
                                       (ACCUMULATED_PATH, batch_name)))
        self.assertEqual(len(b.get_accumulated_batches()), 1)
        self.assertEqual(b.current_batch.length, 0)

        b.save(holding)

        if (by_max_age):
            sleep(.6)

        b.process()

        self.assertEqual(send_accumulated_batches_method.call_count, 1)
        self.assertEqual(len(b.get_accumulated_batches()), 2)

        b.save(acesso)

        if (by_max_age):
            sleep(.6)

        b.process()

        self.assertEqual(send_accumulated_batches_method.call_count, 2)
        self.assertEqual(len(b.get_accumulated_batches()), 3)


class TestStream(TestCase):
    def setUp(self):
        if os.path.exists(ROOT_PATH):
            shutil.rmtree(ROOT_PATH)

    def test_initialization_and_accumulation(self):
        holding = PanamahHolding(id='1234', descricao='teste')
        acesso = PanamahAcesso(id='4321', funcionario_ids=['1', '2'])
        secao = PanamahSecao(id='5555', codigo='6666', descricao='teste')

        b = BatchProcessor('auth', 'secret', '12345')

        self.assertTrue(os.path.exists(ROOT_PATH))
        self.assertTrue(os.path.exists(ACCUMULATED_PATH))
        self.assertTrue(os.path.exists(SENT_PATH))

        b.save(holding)

        self.assertEqual(b.current_batch.length, 1)
        self.assertEqual(b.current_batch.size, 107)
        sleep(.5)
        self.assertAlmostEqual(b.current_batch.age, 0.5, delta=0.2)

        b.save(acesso)

        self.assertEqual(b.current_batch.length, 2)
        self.assertEqual(b.current_batch.size, 221)
        sleep(.5)
        self.assertAlmostEqual(b.current_batch.age, 1, delta=0.2)

        b.save(secao)

        self.assertEqual(b.current_batch.length, 3)
        self.assertEqual(b.current_batch.size, 344)
        sleep(.5)
        self.assertAlmostEqual(b.current_batch.age, 1.5, delta=0.2)

        b.delete(holding)

        self.assertEqual(b.current_batch.length, 4)
        self.assertEqual(b.current_batch.size, 429)
        sleep(.5)
        self.assertAlmostEqual(b.current_batch.age, 2, delta=0.2)

        b.delete(secao)

        self.assertEqual(b.current_batch.length, 5)
        self.assertEqual(b.current_batch.size, 512)
        sleep(.5)
        self.assertAlmostEqual(b.current_batch.age, 2.5, delta=0.2)

        b.delete(acesso)

        self.assertEqual(b.current_batch.length, 6)
        self.assertEqual(b.current_batch.size, 596)
        sleep(.5)
        self.assertAlmostEqual(b.current_batch.age, 3, delta=0.2)

        self.assertEqual(
            b.current_batch.json(),
            '[{"data": {"id": "1234", "descricao": "teste"}, "tipo": "HOLDING", "op": "update", "assinanteId": "12345"}, {"data": {"id": "4321", "funcionarioIds": ["1", "2"]}, "tipo": "ACESSO", "op": "update", "assinanteId": "12345"}, {"data": {"id": "5555", "codigo": "6666", "descricao": "teste"}, "tipo": "SECAO", "op": "update", "assinanteId": "12345"}, {"tipo": "HOLDING", "op": "delete", "data": {"id": "1234"}, "assinanteId": "12345"}, {"tipo": "SECAO", "op": "delete", "data": {"id": "5555"}, "assinanteId": "12345"}, {"tipo": "ACESSO", "op": "delete", "data": {"id": "4321"}, "assinanteId": "12345"}]'
        )

        b.save(holding)

        self.assertEqual(b.current_batch.length, 6)

        self.assertEqual(
            b.current_batch.json(),
            '[{"data": {"id": "4321", "funcionarioIds": ["1", "2"]}, "tipo": "ACESSO", "op": "update", "assinanteId": "12345"}, {"data": {"id": "5555", "codigo": "6666", "descricao": "teste"}, "tipo": "SECAO", "op": "update", "assinanteId": "12345"}, {"tipo": "HOLDING", "op": "delete", "data": {"id": "1234"}, "assinanteId": "12345"}, {"tipo": "SECAO", "op": "delete", "data": {"id": "5555"}, "assinanteId": "12345"}, {"tipo": "ACESSO", "op": "delete", "data": {"id": "4321"}, "assinanteId": "12345"}, {"data": {"id": "1234", "descricao": "teste"}, "tipo": "HOLDING", "op": "update", "assinanteId": "12345"}]'
        )

    def test_expiration_by_max_length(self):
        test_expiration(self, by_max_length=True)

    def test_expiration_by_max_size(self):
        test_expiration(self, by_max_size=True)

    def test_expiration_by_max_age(self):
        test_expiration(self, by_max_age=True)

    def test_sending_batch(self):
        holding = PanamahHolding(id='1234', descricao='teste')
        acesso = PanamahAcesso(id='4321', funcionario_ids=['1', '2'])
        secao = PanamahSecao(id='5555', codigo='6666', descricao='teste')

        b = BatchProcessor('auth', 'secret', '12345', batch_max_length=6)

        b.save(holding)
        b.save(acesso)
        b.save(secao)

        b.delete(holding)
        b.delete(secao)
        b.delete(acesso)

        start_test_server()
        try:
            b.process()
            b.process()

            request = get_last_request()

            expected_payload = [{'data': {'id': '1234', 'descricao': 'teste'}, 'tipo': 'HOLDING', 'op': 'update', 'assinanteId': '12345'}, {'data': {'id': '4321', 'funcionarioIds': ['1', '2']}, 'tipo': 'ACESSO', 'op': 'update', 'assinanteId': '12345'}, {'data': {'id': '5555', 'codigo': '6666', 'descricao': 'teste'},
                                                                                                                                                                                                                                                              'tipo': 'SECAO', 'op': 'update', 'assinanteId': '12345'}, {'tipo': 'HOLDING', 'op': 'delete', 'data': {'id': '1234'}, 'assinanteId': '12345'}, {'tipo': 'SECAO', 'op': 'delete', 'data': {'id': '5555'}, 'assinanteId': '12345'}, {'tipo': 'ACESSO', 'op': 'delete', 'data': {'id': '4321'}, 'assinanteId': '12345'}]

            self.assertListEqual(request['payload'], expected_payload)
        finally:
            stop_test_server()

    def test_flushing(self):
        holding = PanamahHolding(id='1234', descricao='teste')
        acesso = PanamahAcesso(id='4321', funcionario_ids=['1', '2'])
        secao = PanamahSecao(id='5555', codigo='6666', descricao='teste')

        b = BatchProcessor('auth', 'secret', '12345', batch_max_length=9999)

        b.save(holding)
        b.save(acesso)
        b.save(secao)

        b.delete(holding)
        b.delete(secao)
        b.delete(acesso)

        start_test_server()
        try:
            b.process()
            b.flush()

            request = get_last_request()

            expected_payload = [{'data': {'id': '1234', 'descricao': 'teste'}, 'tipo': 'HOLDING', 'op': 'update', 'assinanteId': '12345'}, {'data': {'id': '4321', 'funcionarioIds': ['1', '2']}, 'tipo': 'ACESSO', 'op': 'update', 'assinanteId': '12345'}, {'data': {'id': '5555', 'codigo': '6666', 'descricao': 'teste'},
                                                                                                                                                                                                                                                              'tipo': 'SECAO', 'op': 'update', 'assinanteId': '12345'}, {'tipo': 'HOLDING', 'op': 'delete', 'data': {'id': '1234'}, 'assinanteId': '12345'}, {'tipo': 'SECAO', 'op': 'delete', 'data': {'id': '5555'}, 'assinanteId': '12345'}, {'tipo': 'ACESSO', 'op': 'delete', 'data': {'id': '4321'}, 'assinanteId': '12345'}]

            self.assertListEqual(request['payload'], expected_payload)
        finally:
            stop_test_server()

    def test_requesting_pending_resources(self):
        b = BatchProcessor('auth', 'secret', '12345')

        with mock.patch.object(b.client, 'get') as get_method:
            get_method.return_value = Response(200, {
                "00934509022": {
                    "HOLDING": [
                        "07128945000132"
                    ],
                    "LOJA": [
                        "111"
                    ],
                    "PRODUTO": [
                        "1"
                    ],
                    "SECAO": [
                        "xxxx"
                    ]
                },
                "02541926375": {
                    "LOJA": [
                        "111",
                        "2345"
                    ],
                    "PRODUTO": [
                        "1"
                    ],
                    "SECAO": [
                        "xxxx"
                    ]
                }
            })

            (page, count) = b.request_pending_resources()

            self.assertEqual(count, 2)
            self.assertDictEqual(page, {'00934509022': {'HOLDING': ['07128945000132'], 'LOJA': ['111'], 'PRODUTO': [
                                 '1'], 'SECAO': ['xxxx']}, '02541926375': {'LOJA': ['111', '2345'], 'PRODUTO': ['1'], 'SECAO': ['xxxx']}})

            get_method.return_value = Response(200, {
                "00934509022": {
                    "SECAO": [
                        "zzzz"
                    ]
                },
                "02541926375": {
                    "LOJA": [
                        "3333"
                    ],
                    "PRODUTO": [
                        "2"
                    ]
                }
            })

            (page2, count) = b.request_pending_resources(concat=page)

            self.assertEqual(count, 2)
            self.assertDictEqual(page2, {'00934509022': {'HOLDING': ['07128945000132'], 'LOJA': ['111'], 'PRODUTO': ['1'], 'SECAO': [
                                 'xxxx', 'zzzz']}, '02541926375': {'LOJA': ['111', '2345', '3333'], 'PRODUTO': ['1', '2'], 'SECAO': ['xxxx']}})

            get_method.return_value = Response(200, {})

            (page3, count) = b.request_pending_resources(concat=page)

            self.assertEqual(count, 0)
            self.assertDictEqual(page3, {'00934509022': {'HOLDING': ['07128945000132'], 'LOJA': ['111'], 'PRODUTO': ['1'], 'SECAO': [
                                 'xxxx', 'zzzz']}, '02541926375': {'LOJA': ['111', '2345', '3333'], 'PRODUTO': ['1', '2'], 'SECAO': ['xxxx']}})

    def test_get_pending_resources(self):
        processor = BatchProcessor('auth', 'secret', '12345')

        def fake_request_pending_resources(start=0, count=100, concat=None):
            resources = {
                "00934509022": {
                    "SECAO": [
                        "zzzz"
                    ]
                },
                "02541926375": {
                    "LOJA": [
                        "3333"
                    ],
                    "PRODUTO": [
                        "2"
                    ]
                }
            }
            if start == 0:
                return (resources, 2)
            else:
                return (resources, 0)
        with mock.patch.object(processor, 'request_pending_resources', side_effect=fake_request_pending_resources):
            resources = processor.get_pending_resources()
            self.assertEqual(len(resources), 2)
            self.assertTrue(isinstance(
                resources['00934509022'][0], PanamahSecao))
            self.assertTrue(isinstance(
                resources['02541926375'][0], PanamahLoja))
            self.assertTrue(isinstance(
                resources['02541926375'][1], PanamahProduto))

    def test_recover_failures(self):
        processor = BatchProcessor(
            'auth', 'secret', '12345', batch_max_length=1
        )

        holding = PanamahHolding(id='1234', descricao='teste')
        batch = Batch()
        batch_filename = batch.filename
        batch.append(Update.from_model(holding))
        batch.save(directory=ACCUMULATED_PATH)

        loaded_batch = Batch(filename='%s/%s' %
                             (ACCUMULATED_PATH, batch_filename))
        mock_response = {
            'falhas': {
                'total': 1,
                'itens': loaded_batch.operations
            }
        }
        processor.recover_from_failures(loaded_batch, mock_response)
        self.assertTrue(bool(next((file for file in os.listdir(
            ACCUMULATED_PATH) if file.startswith('0_')), False)))


if __name__ == '__main__':
    main()
