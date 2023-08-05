from os import environ
from .models.definitions import PanamahAssinante
from .client import AdminClient
from .exceptions import NotFoundException, AdminException, ConflictException

ENVIRONMENT_AUTHORIZATION_TOKEN = environ.get('PANAMAH_AUTHORIZATION_TOKEN')


class PanamahAdmin():
    class _PanamahAdmin():
        def __init__(self, authorization_token):
            self.authorization_token = authorization_token
            self.client = AdminClient(authorization_token)

        def get_assinante(self, id):
            response = self.client.get('/admin/assinantes/' + id)
            if response.status_code == 200:
                return PanamahAssinante.from_json(response.json())
            elif response.status_code == 404:
                raise NotFoundException('Assinante nao existe.')
            else:
                raise AdminException(
                    'Erro %d ao tentar buscar um assinante.' % response.status_code
                )

        def create_assinante(self, assinante):
            response = self.client.post('/admin/assinantes', assinante.json(dumps=False))
            if response.status_code == 201:
                return PanamahAssinante.from_json(response.json())
            elif response.status_code == 409:
                raise ConflictException('Assinante ja existe.')
            else:
                raise AdminException(
                    'Erro %d ao criar um assinante.' % response.status_code
                )

        def delete_assinante(self, id):
            response = self.client.delete(
                '/admin/assinantes/' + id, payload=None
            )
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                raise ConflictException('Assinante nao existe.')
            else:
                raise AdminException(
                    'Erro %d ao deletar um assinante.' % response.status_code
                )

    instance = None

    def __init__(self, authorization_token=ENVIRONMENT_AUTHORIZATION_TOKEN):
        if self.instance is None:
            self.instance = PanamahAdmin._PanamahAdmin(authorization_token)
        PanamahAdmin.authorization_token = authorization_token

    def __getattr__(self, name):
        return getattr(self.instance, name)
