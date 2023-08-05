import os
import hashlib
import glob
from time import sleep
from threading import Thread
from datetime import datetime
from .client import StreamClient
from .batch import Batch
from .exceptions import DataException
from .operation import Operation, Update, Delete
from .models.definitions import from_json as model_from_json

ROOT_PATH = './.panamah'
ACCUMULATED_PATH = ROOT_PATH + '/accumulated'
SENT_PATH = ROOT_PATH + '/sent'
BATCH_MAX_LENGTH = 500
BATCH_MAX_SIZE = 5 * 1024
BATCH_MAX_AGE = 5 * 60


class BatchProcessor(Thread):
    def __init__(self, authorization_token, secret, assinante_id, batch_max_length=BATCH_MAX_LENGTH, batch_max_size=BATCH_MAX_SIZE, batch_max_age=BATCH_MAX_AGE):
        Thread.__init__(self, daemon=True)
        self.initialize_structure()
        self.assinante_id = assinante_id
        self.multitenancy = assinante_id == '*'
        self.client = StreamClient(authorization_token, secret, assinante_id)
        self.current_batch = Batch(
            filename='%s/%s' % (ROOT_PATH, 'current.pbt'), force_existence=True)
        self.last_batch_hash = None
        self.batch_max_length = batch_max_length
        self.batch_max_size = batch_max_size
        self.batch_max_age = batch_max_age

    def run(self):
        while True:
            self.initialize_structure()
            self.process()

    def initialize_structure(self):
        if not os.path.exists(ACCUMULATED_PATH):
            os.makedirs(ACCUMULATED_PATH)
        if not os.path.exists(SENT_PATH):
            os.makedirs(SENT_PATH)

    def process(self):
        if self.accumulated_batch_exists():
            self.send_accumulated_batches()
        self.watch_current_batch()
        self.delete_old_batches()

    def accumulated_batch_exists(self):
        return len([file for file in os.listdir(ACCUMULATED_PATH) if file.endswith('.pbt')]) > 0

    def send_accumulated_batches(self):
        batches = self.get_accumulated_batches()
        for batch in batches:
            response = self.client.post('/stream/data', batch.json(dumps=False))
            if response.status_code == 200:
                response_data = response.json()
                if hasattr(response_data, 'falhas'):
                    self.recover_from_failures(batch, response_data.falhas)
                    break
                else:
                    batch.move(source=ACCUMULATED_PATH, destiny=SENT_PATH)
            else:
                raise DataException()

    def watch_current_batch(self):
        if self.current_batch_expired():
            self.accumulate_current_batch()
        else:
            self.write_changes_to_current_batch()

    def delete_old_batches(self):
        sent_batches = [Batch(filename='%s/%s' % (SENT_PATH, file))
                        for file in os.listdir(SENT_PATH) if file.endswith('.pbt')]
        old_batches = [
            batch for batch in sent_batches if self.current_batch.age > 24 * 60 * 60]
        if len(old_batches) > 0:
            for batch in old_batches:
                batch.delete(SENT_PATH)

    def current_batch_expired(self):
        def expired_by_count():
            return self.current_batch.length >= self.batch_max_length

        def expired_by_size():
            return self.current_batch.size >= self.batch_max_size

        def expired_by_time():
            return self.current_batch.age >= self.batch_max_age

        return expired_by_count() or expired_by_size() or expired_by_time()

    def accumulate_current_batch(self):
        if self.current_batch.length > 0:
            self.current_batch.save(
                directory=ACCUMULATED_PATH, filename=self.current_batch.get_filename_by_created_date())
            self.current_batch.reset()

    def write_changes_to_current_batch(self):
        self.current_batch_hash = self.current_batch.hash()
        if self.current_batch_hash != self.last_batch_hash:
            self.current_batch.save(
                directory=ROOT_PATH,
                filename='current.pbt'
            )
            self.last_batch_hash = self.current_batch.hash()

    def get_accumulated_batches(self):
        return [Batch(filename='%s/%s' % (ACCUMULATED_PATH, file))
                for file in os.listdir(ACCUMULATED_PATH) if file.endswith('.pbt')]

    def recover_from_failures(self, batch, failures):
        if failures['falhas']['total'] > 0:
            failed_ids = [Operation.from_json(
                item).id for item in failures['falhas']['itens']]
            failed_operations = [Operation.from_json(operation) for operation in batch.operations
                                 if next((failed_id for failed_id in failed_ids
                                          if failed_id == Operation.from_json(operation).id
                                          ), False)]
            prioritized_batch = Batch(
                operations=failed_operations,
                high_priority=True
            )
            prioritized_batch.save(directory=ACCUMULATED_PATH)

    def save(self, model, assinante_id=None):
        if self.multitenancy and assinante_id is None:
            raise ValueError('assinante_id e requerido no modo multitenancy')
        model.validate()
        operation = Update.from_model(model, assinante_id if assinante_id else self.assinante_id)
        self.current_batch.remove(operation).append(operation)

    def delete(self, model, assinante_id=None):
        if self.multitenancy and assinante_id is None:
            raise ValueError('assinante_id e requerido no modo multitenancy')
        if hasattr(model, 'id'):
            self.current_batch.append(Delete.from_model(model, assinante_id if assinante_id else self.assinante_id))
        else:
            raise ValueError('id obrigatorio para exclusao')

    def request_pending_resources(self, start=0, count=100, concat=None):
        result = concat if concat is not None else {}
        response = self.client.get(
            '/stream/pending-resources?start=%d&count=%d' % (start, count))
        count = 0
        if response.status_code == 200:
            data = response.json()
            count = len(data)
            for assinante_id, value in data.items():
                for modelName, ids in value.items():
                    if assinante_id not in result:
                        result[assinante_id] = {}
                    if modelName not in result[assinante_id]:
                        result[assinante_id][modelName] = []
                    result[assinante_id][modelName] = result[assinante_id][modelName] + ids
        else:
            raise DataException('Erro ao buscar recursos pendentes.')
        return (result, count)

    def get_pending_resources(self):
        start = 0
        count = 100
        (pending_resources, count) = self.request_pending_resources()
        while count > 0:
            (pending_resources, count) = self.request_pending_resources(
                start + count,
                count,
                concat=pending_resources
            )
        result = {}
        for assinante_id, value in pending_resources.items():
            if assinante_id not in result:
                result[assinante_id] = []
            for modelName, ids in value.items():
                for id in ids:
                    result[assinante_id].append(model_from_json(modelName, {'id': id}))
        return result

    def flush(self):
        self.accumulate_current_batch()
        self.send_accumulated_batches()
