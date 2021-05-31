import os
from json_parser import IngredientsJsonDecoder, Candy

path = os.path.dirname(__file__)


def json_to_candy():
    ingredients_decoder = IngredientsJsonDecoder()
    filename = os.path.join(path, 'candy_json/candy_long.json')
    file = open(filename)
    candy_json = file.read().replace("\n", " ")
    return Candy.from_json(candy_json, ingredients_decoder)


def test_candy(benchmark):
    benchmark(json_to_candy)
