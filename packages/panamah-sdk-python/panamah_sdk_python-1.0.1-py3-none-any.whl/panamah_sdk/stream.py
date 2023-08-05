import time
import atexit
from os import environ
from events import Events
from .models.base import Model
from .processor import BatchProcessor
from .nfe import Nfe

ENVIRONMENT_AUTHORIZATION_TOKEN = environ.get('PANAMAH_AUTHORIZATION_TOKEN')
ENVIRONMENT_SECRET = environ.get('PANAMAH_SECRET')
ENVIRONMENT_ASSINANTE_ID = environ.get('PANAMAH_ASSINANTE_ID')


class BoolHook:
    def __init__(self, initial_result=True):
        self.result = initial_result

    def set_false(self):
        self.result = False

    def set_true(self):
        self.result = True


class PanamahStream():
    class _PanamahStream():
        def __init__(self, authorization_token, secret, assinante_id):
            self.authorization_token = authorization_token
            self.secret = secret
            self.assinante_id = assinante_id
            self.processor = BatchProcessor(
                authorization_token, secret, assinante_id)
            self.processor.start()
            self.events = Events()

            def flush():
                try:
                    self.processor.flush()
                except Exception as e:
                    print('Flushing falhou com: ', str(e))
            atexit.register(flush)

        def is_acceptable_model(self, model):
            return hasattr(model, 'name') and model.name != 'ASSINANTE'

        def emit(self, event, *args):
            event_slot = getattr(self.events, event)
            event_slot(*args)

        def on(self, event, fn):
            event_slot = getattr(self.events, event)
            event_slot += fn

        def off(self, event, fn):
            event_slot = getattr(self.events, event)
            event_slot -= fn

        def save(self, model, assinante_id=None):
            models = model if isinstance(model, list) else [model]
            for item in models:
                if isinstance(item, Model) and self.is_acceptable_model(item):
                    allow_save = BoolHook()
                    self.emit('before_save', item, allow_save.set_false)
                    if allow_save.result:
                        self.processor.save(item, assinante_id)
                else:
                    raise ValueError(
                        'model deve ser um modelo valido do Panamah')

        def delete(self, model, assinante_id=None):
            models = model if isinstance(model, list) else [model]
            for item in models:
                if isinstance(item, Model) and self.is_acceptable_model(item):
                    allow_delete = BoolHook()
                    self.emit('before_delete', item, allow_delete.set_false)
                    if allow_delete.result:
                        self.processor.delete(item, assinante_id)
                else:
                    raise ValueError(
                        'model deve ser um modelo valido do Panamah')

        def flush(self):
            self.processor.flush()

        def read_nfe(self, filename):
            return Nfe.read_models_from_file(filename)

        def read_nfe_directory(self, dirname):
            return Nfe.read_models_from_directory(dirname)

    instance = None

    def __init__(self, authorization_token=ENVIRONMENT_AUTHORIZATION_TOKEN, secret=ENVIRONMENT_SECRET, assinante_id=ENVIRONMENT_ASSINANTE_ID or '*'):
        if self.instance is None:
            self.instance = PanamahStream._PanamahStream(
                authorization_token, secret, assinante_id)
        PanamahStream.authorization_token = authorization_token
        PanamahStream.secret = secret
        PanamahStream.assinante_id = assinante_id

    def __getattr__(self, name):
        return getattr(self.instance, name)
