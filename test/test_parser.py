import pytest
from json_parser import interface_decoder, ClassMapLookUpFailError, InterfaceDecoder, JSONPrimitive, Dict, \
    IngredientsJsonDecoder, Candy, NaturalIngredient, ArtificialIngredient, FromJson
import os.path

path = os.path.dirname(__file__)


def test_candy_from_json():
    ingredients_decoder = IngredientsJsonDecoder()
    filename = os.path.join(path, 'candy_json/candy.json')
    file = open(filename)
    candy_json = file.read().replace("\n", " ")
    candy_object = Candy.from_json(candy_json, ingredients_decoder)
    assert candy_object.price == 3.14
    assert candy_object.ingredients.__len__() == 4
    assert sum(isinstance(x, NaturalIngredient) for x in candy_object.ingredients) == 2
    assert sum(isinstance(x, ArtificialIngredient) for x in candy_object.ingredients) == 2


def test_person_from_json():
    class Person(FromJson):
        def __init__(self, first_name: str, last_name: str):
            self.first_name = first_name
            self.last_name = last_name

        @classmethod
        def from_json_dict(cls, d: Dict[str, JSONPrimitive], decoder: InterfaceDecoder):
            return Person(d['first_name'], d['last_name'])

        def __eq__(self, other: 'Person'):
            return self.first_name == other.first_name and self.last_name == other.last_name

    person_decoder = InterfaceDecoder({'Person': Person})
    got = person_decoder.from_json_dict({'__type__': 'Person',
                                         'first_name': 'John',
                                         'last_name': 'Doe'})
    expected = Person('John', 'Doe')
    assert got == expected


def test_dict_from_json():
    raw = """{
      "__type__": "dict",
      "__data__": [
        {
          "key": "a",
          "value": "b"
        },
        {
          "key": "c",
          "value": "d"
        }
      ]
    }"""
    d = interface_decoder.from_json(raw)
    assert d == {'a': 'b', 'c': 'd'}


def test_lookup_fail():
    with pytest.raises(ClassMapLookUpFailError):
        interface_decoder.from_json_dict({'__type__': 'User',
                                          'first_name': 'John',
                                          'last_name': 'Doe'})
