from unittest import main, mock, TestCase
from panamah_sdk.batch import Batch
from panamah_sdk.operation import Operation, Update, Delete
from panamah_sdk.models.definitions import PanamahHolding


class TestBatch(TestCase):
    def test_batch(self):
        holding = PanamahHolding(id='1234', descricao='teste')
        batch = Batch()
        batch.append(Update.from_model(holding))
        self.assertEqual(batch.json(), '[{"data": {"id": "1234", "descricao": "teste"}, "tipo": "HOLDING", "op": "update"}]')
        batch.append(Delete.from_model(holding))
        self.assertEqual(batch.json(), '[{"data": {"id": "1234", "descricao": "teste"}, "tipo": "HOLDING", "op": "update"}, {"tipo": "HOLDING", "op": "delete", "data": {"id": "1234"}}]')

if __name__ == '__main__':
    main()