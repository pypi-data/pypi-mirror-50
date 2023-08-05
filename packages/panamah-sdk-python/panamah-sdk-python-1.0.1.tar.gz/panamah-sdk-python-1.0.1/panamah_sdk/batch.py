import base64
import hashlib
import os
import shutil
import json
from datetime import datetime
from .operation import Operation

FILENAME_FORMAT = '%Y_%m_%d_%H_%M_%S_%f.pbt'


class Batch():
    def __init__(self, filename=None, force_existence=False, operations=None, high_priority=False):
        self.high_priority = high_priority
        self.filename = filename
        if filename is not None:
            if force_existence:
                self.force_existence(filename)
            self.created_at = datetime.strptime(os.path.basename(
                filename), FILENAME_FORMAT) if self.filename_conforms(filename, FILENAME_FORMAT) else datetime.now()
            self.filename = os.path.basename(filename)
            self.operations = self.read_operations(filename)
        else:
            self.reset()
        if operations is not None:
            self.operations = operations

    @property
    def size(self):
        return len(self.json())

    @property
    def length(self):
        return len(self.operations)

    @property
    def age(self):
        return (datetime.now() - self.created_at).total_seconds()

    def force_existence(self, filename):
        if not os.path.exists(filename):
            with open(filename, mode='w') as fp:
                fp.write('[]')

    def save(self, directory, filename=None):
        with open('%s/%s' % (directory, filename if filename is not None else self.filename), mode='w+') as fp:
            return fp.write(self.json())

    def move(self, source, destiny):
        source_filename = '%s/%s' % (source, self.filename)
        destiny_filename = '%s/%s' % (destiny, self.filename)
        try:
            if os.path.exists(source_filename):
                shutil.move(src=source_filename, dst=destiny_filename)
        except:
            pass

    def json(self, dumps=True):
        operations = [operation.json(dumps=False) if isinstance(operation, Operation) else operation for operation in self.operations]
        return json.dumps(operations) if dumps else operations

    def read_operations(self, filename):
        content = self.read_content(filename)
        return json.loads(content) if content else []

    def read_content(self, filename):
        if os.path.exists(filename):
            with open(filename, mode='r') as fp:
                return fp.read()
        return None

    def filename_conforms(self, filename, expected_format):
        try:
            datetime.strptime(os.path.basename(filename), expected_format)
            return True
        except:
            return False

    def append(self, operation):
        self.operations.append(operation)
        return self

    def remove(self, operation):
        found = list(filter(lambda batchOperation:            
            batchOperation.id == operation.id and
            batchOperation.assinanteId == operation.assinanteId and
            batchOperation.tipo == operation.tipo and
            batchOperation.op == operation.op,
            self.operations
        ))
        if len(found) > 0:
            self.operations.remove(found[0])
        return self

    def get_filename_by_created_date(self):
        filename = self.created_at.strftime(FILENAME_FORMAT)
        if self.high_priority:
            filename = '0_' + filename
        return filename

    def reset(self):
        self.created_at = datetime.now()
        self.filename = self.get_filename_by_created_date()
        self.operations = []

    def hash(self):
        return base64.b64encode(hashlib.sha1(self.json().encode('utf-8')).digest()).decode('utf-8')
