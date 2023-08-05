import json
from datetime import datetime, date
from dateutil.parser import parse as parse_date


class Model():
    schema = {}

    def __init__(self, **kwargs):
        self.values = {}
        if kwargs is not None:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __getattr__(self, name):
        if name in self.schema:
            if name in self.values:
                return self.values[name]
            else:
                return self.schema[name].default if hasattr(self.schema[name], 'default') else None
        elif name in ['values', 'name']:
            super(Model, self).__getattribute__(name)
        else:
            raise NameError("%s nao e uma propriedade do modelo" % name)

    def __setattr__(self, name, value):
        if name in self.schema:
            field = self.schema[name]
            if value is None:
                self.values[name] = None
            else:
                self.values[name] = field.cast(
                    value) if hasattr(field, 'cast') else value
        elif name == 'values':
            super(Model, self).__setattr__(name, value)
        else:
            raise NameError("%s nao e uma propriedade do modelo" % name)

    @classmethod
    def get_field_by_json_key(cls, json_name):
        for key in cls.schema:
            field = cls.schema[key]
            if hasattr(field, 'json_name') and field.json_name == json_name:
                return field, key
        return None, None

    def validate(self):
        for name, field in self.schema.items():
            try:
                field.validate(getattr(self, name))
            except Exception as error:
                raise type(error)('%s.%s -> %s' %
                                  (self.__class__.__name__, name, str(error)))

    def json(self, dumps=True):
        result = {}
        for key, value in self.values.items():
            field = self.schema[key]
            json_key = field.json_name if field.json_name else key
            if isinstance(value, Model):
                result[json_key] = value.json(dumps=False)
            elif isinstance(value, list):
                result[json_key] = [item.json(dumps=False) if isinstance(
                    item, Model) else item for item in value]
            else:
                if hasattr(field, 'to_json'):
                    result[json_key] = field.to_json(value)
                else:
                    result[json_key] = value
        return json.dumps(result) if dumps else result

    @classmethod
    def from_json(cls, json):
        result = cls()
        for key, value in json.items():
            field_by_json, schema_key = cls.get_field_by_json_key(key)
            if key in cls.schema or field_by_json:
                field = field_by_json if field_by_json else cls.schema[key]
                object_key = schema_key if schema_key else key
                def deserialize(field, value):
                    if hasattr(field, 'from_json'):
                        return field.from_json(value)
                    else:
                        return value
                if isinstance(value, list):
                    setattr(result, object_key, [deserialize(field, item) if isinstance(
                        item, object) else item for item in value])
                else:
                    setattr(result, object_key, deserialize(field, value))
        return result


class Field():
    def __init__(self, type='unknown', required=False, default=None, json_name=None):
        self.type = type
        self.required = required
        self.default = default
        self.json_name = json_name

    def validate(self, value):
        if self.required and value is None:
            raise ValueError('propriedade obrigatoria')


class StringField(Field):
    def __init__(self, allowedValues=None, required=False, default=None, json_name=None):
        self.allowedValues = allowedValues
        super().__init__('string', required, default, json_name)

    def validate(self, value):
        super().validate(value)
        if self.allowedValues is not None:
            invalid_items = [
                item for item in value if item not in self.allowedValues
            ]
            if len(invalid_items) > 0:
                raise ValueError(
                    'valor(es) "%s" nao permitido(s). Somente %s' % (
                        ', '.join(invalid_items),
                        ', '.join(self.allowedValues)
                    )
                )

    def cast(self, value):
        return str(value)


class NumberField(Field):
    def __init__(self, required=False, default=None, json_name=None):
        super().__init__('number', required, default, json_name)

    def cast(self, value):
        return float(value)


class BooleanField(Field):
    def __init__(self, required=False, default=None, json_name=None):
        super().__init__('date', required, default, json_name)

    def cast(self, value):
        return bool(value)


class DateField(Field):
    def __init__(self, required=False, default=None, json_name=None):
        super().__init__('boolean', required, default, json_name)

    def cast(self, value):
        if isinstance(value, str):
            return parse_date(value)
        elif isinstance(value, int):
            return datetime.utcfromtimestamp(value)
        elif isinstance(value, date):
            return value
        else:
            raise ValueError('data invalida')

    def to_json(self, value):
        return value.isoformat()

    def from_json(self, value):
        return self.cast(value)


class StringListField(Field):
    def __init__(self, allowedValues=None, required=False, default=None, json_name=None):
        self.allowedValues = allowedValues
        super().__init__('list[string]', required, default, json_name)

    def validate(self, value):
        super().validate(value)
        if self.allowedValues is not None:
            invalid_items = [
                item for item in value if item not in self.allowedValues
            ]
            if len(invalid_items) > 0:
                raise ValueError(
                    'valor(es) "%s" nao permitido(s). Somente %s' % (
                        ', '.join(invalid_items),
                        ', '.join(self.allowedValues)
                    )
                )


class ObjectField(Field):
    def __init__(self, object_class=None, required=False, default=None, json_name=None):
        self.object_class = object_class
        super().__init__('object', required, default, json_name)

    def validate(self, value):
        super().validate(value)
        if value is not None:
            if type(value) is self.object_class:
                value.validate()
            else:
                raise ValueError(
                    'valor deve ser um modelo valido do tipo %s' % self.object_class.__name__)

    def from_json(self, value):
        return self.object_class.from_json(value)


class ObjectListField(Field):
    def __init__(self, object_class=None, required=False, default=None, json_name=None):
        self.object_class = object_class
        super().__init__('list[object]', required, default, json_name)

    def validate(self, value):
        super().validate(value)
        if value is not None:
            invalid_indexes = [
                index for (index, item) in enumerate(value) if not type(item) is self.object_class
            ]
            if len(invalid_indexes) == 0:
                for item in value:
                    item.validate()
            else:
                raise ValueError(
                    'objeto(s) no(s) indice(s) %s deve(m) ser modelo(s) valido(s) do tipo %s' % (
                        ', '.join([str(index) for index in invalid_indexes]
                                  ), self.object_class.__name__
                    )
                )
