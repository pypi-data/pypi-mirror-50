import json
from .models.base import Model


class Operation():
    def __init__(self, data, tipo, op, assinanteId, id):
        self.id = id
        self.data = data
        self.op = op
        self.tipo = tipo
        self.assinanteId = assinanteId

    @classmethod
    def from_model(cls, op, model, assinanteId):
        data = model
        tipo = model.name
        id = model.id
        return Operation(data, tipo, op, assinanteId, id)

    @classmethod
    def from_json(cls, json):
        data = json['data']
        tipo = json['tipo']
        id = data['id'] if 'id' in data else json['id']
        op = json['op']
        assinanteId = data['assinanteId'] if 'assinanteId' in json else None
        return Operation(data, tipo, op, assinanteId, id)

    def json(self, dumps=True):
        result = {
            'data': self.data.json(dumps=False) if isinstance(self.data, Model) else self.data,
            'tipo': self.tipo,
            'op': self.op
        }
        if self.op == 'delete':
            del result['data']
            if hasattr(self.data, 'id'):
                result['data'] = { 'id': self.data.id }
            if self.id is not None:
                result['data'] = { 'id': self.id }
        if self.assinanteId is not None:
            result['assinanteId'] = self.assinanteId
        return json.dumps(result) if dumps else result

class Update(Operation):
    def __init__(self, data, tipo, op, assinanteId, id):
        super().__init__(data, tipo, 'update', assinanteId, id)

    @classmethod
    def from_model(cls, model, assinanteId=None):
        return super().from_model('update', model, assinanteId)

class Delete(Operation):
    def __init__(self, data, tipo, op, assinanteId, id):
        super().__init__(data, tipo, 'delete', assinanteId, id)

    @classmethod
    def from_model(cls, model, assinanteId=None):
        return super().from_model('delete', model, assinanteId)