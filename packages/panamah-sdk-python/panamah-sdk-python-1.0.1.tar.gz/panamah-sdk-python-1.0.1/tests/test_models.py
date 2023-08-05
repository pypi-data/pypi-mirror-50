import json
import unittest
from datetime import date
from panamah_sdk.models.definitions import Model, StringField, NumberField, BooleanField, DateField, ObjectField, StringListField, ObjectListField


def validate_then_expect(self, instance, message):
    try:
        instance.validate()
    except Exception as e:
        self.assertEqual(str(e), message, "Message expected")
        pass


def validate_then_dont_expect(self, instance, message):
    try:
        instance.validate()
    except Exception as e:
        if message == '*':
            raise 'Exception not expected'
        self.assertNotEqual(str(e), message, "Message not expected")
        pass


class GrandChildModel(Model):
    schema = {
        'z': StringField(required=True)
    }


class WrongChildModel(Model):
    pass


class ChildModel(Model):
    schema = {
        'i': StringField(required=False),
        'j': ObjectField(required=False, object_class=GrandChildModel),
        'l': ObjectListField(required=False, object_class=GrandChildModel)
    }


class ParentModel(Model):
    schema = {
        'a': StringField(required=True),
        'b': StringField(required=True, allowedValues=['1', '2']),
        'c': StringListField(required=True, allowedValues=['1', '2']),
        'd': NumberField(required=True),
        'e': BooleanField(required=True),
        'f': DateField(required=True),
        'g': ObjectField(required=True, object_class=ChildModel),
        'h': ObjectListField(required=True, object_class=ChildModel),
        'aliased': StringField(required=False, json_name='aLiAsEd'),
    }


class TestClient(unittest.TestCase):

    def test_field_validations(self):
        # Initialization
        instance = ParentModel(a='1')
        self.assertEqual(instance.a, '1')

        # Required
        instance = ParentModel()
        validate_then_expect(
            self, instance, 'ParentModel.a -> propriedade obrigatoria')
        instance.a = 'valor preenchido'
        validate_then_dont_expect(
            self, instance, 'ParentModel.a -> propriedade obrigatoria')
        self.assertEqual(instance.a, 'valor preenchido')

        # StringField with allowedValues
        instance.b = '3'
        validate_then_expect(
            self, instance, 'ParentModel.b -> valor(es) "3" nao permitido(s). Somente 1, 2')
        instance.b = '1'
        validate_then_dont_expect(
            self, instance, 'ParentModel.b -> valor(es) "3" nao permitido(s). Somente 1, 2')

        # StringListField
        instance.c = ['1', '2', '3']
        validate_then_expect(
            self, instance, 'ParentModel.c -> valor(es) "3" nao permitido(s). Somente 1, 2')
        instance.c = ['1', '2']
        validate_then_dont_expect(
            self, instance, 'ParentModel.c -> valor(es) "3" nao permitido(s). Somente 1, 2')

        # NumberField
        instance.d = '333'
        self.assertEqual(instance.d, 333)

        # BooleanField
        instance.e = 1
        self.assertEqual(instance.e, True)
        instance.e = 0
        self.assertEqual(instance.e, False)

        # DateField
        try:
            instance.f = .0
        except Exception as e:
            self.assertEqual(str(e), 'data invalida')
        instance.f = '2019-01-03T23:59:58'
        self.assertEqual(instance.f.year, 2019)
        self.assertEqual(instance.f.month, 1)
        self.assertEqual(instance.f.day, 3)
        self.assertEqual(instance.f.hour, 23)
        self.assertEqual(instance.f.minute, 59)
        self.assertEqual(instance.f.second, 58)
        instance.f = 1546559998
        self.assertEqual(instance.f.year, 2019)
        self.assertEqual(instance.f.month, 1)
        self.assertEqual(instance.f.day, 3)
        self.assertEqual(instance.f.hour, 23)
        self.assertEqual(instance.f.minute, 59)
        self.assertEqual(instance.f.second, 58)

        # ObjectField
        instance.g = ChildModel()
        validate_then_dont_expect(
            self, instance, 'ParentModel.g -> ChildModel.j -> valor deve ser um modelo valido do tipo GrandChildModel')
        validate_then_dont_expect(
            self, instance, 'ParentModel.g -> ChildModel.l -> \'NoneType\' object is not iterable')
        instance.g = WrongChildModel()
        validate_then_expect(
            self, instance, 'ParentModel.g -> valor deve ser um modelo valido do tipo ChildModel')
        instance.g = ChildModel()
        validate_then_dont_expect(
            self, instance, 'ParentModel.g -> valor deve ser um modelo valido do tipo ChildModel')

        # ObjectListField
        instance.h = [WrongChildModel(), ChildModel()]
        validate_then_expect(
            self, instance, 'ParentModel.h -> objeto(s) no(s) indice(s) 0 deve(m) ser modelo(s) valido(s) do tipo ChildModel')
        instance.h = [ChildModel()]
        validate_then_dont_expect(
            self, instance, 'ParentModel.h -> objeto(s) no(s) indice(s) 0 deve(m) ser modelo(s) valido(s) do tipo ChildModel')

    def test_serialization(self):
        instance = ParentModel(
            aliased='123',
            a='1',
            b='2',
            c=['1', '2'],
            d=100,
            e=True,
            f=1546559998,
            g=ChildModel(
                i='foo',
                j=GrandChildModel(z='bar'),
                l=[GrandChildModel(z='foz')]
            ),
            h=[
                ChildModel(i='baz'),
                ChildModel(
                    i='fox',
                    j=GrandChildModel(z='bax'),
                    l=[
                        GrandChildModel(z='xof')
                    ]
                )
            ]
        )

        expected_json = '{"aLiAsEd": "123", "a": "1", "b": "2", "c": ["1", "2"], "d": 100.0, "e": true, "f": "2019-01-03T23:59:58", "g": {"i": "foo", "j": {"z": "bar"}, "l": [{"z": "foz"}]}, "h": [{"i": "baz"}, {"i": "fox", "j": {"z": "bax"}, "l": [{"z": "xof"}]}]}'

        self.assertEqual(
            instance.json(),
            expected_json
        )

        deserialized = ParentModel.from_json(json.loads(expected_json))
        self.assertEqual(deserialized.aliased, '123')


if __name__ == '__main__':
    unittest.main()
