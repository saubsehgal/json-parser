# JsonParser

##### Parser parses the json string and gives the instance of the class on which it is called.

## Features
- One can easily override ```InterfaceDecoder``` or implement interface ```FromJson``` for a Custom Decoder.
- It comes with an ```IngredientsDecoder``` which overrides the ```InterfaceDecoder```
- Decoder accepts a class map object which is a mapping of key to Class.
- A default class map has been provided for ```IngredientsDecoder``` which maps naturalIngredients to 
```NaturalIngredient``` object and artificialIngredients to ```ArtificialIngredient``` object. 
  (See the swagger for sample json)
- All the Class objects - Candy and Ingredients implement the interface.
- For low level JSON parsing simdjson is used.

# Install

```
pip install git+git://github.com/saubsehgal/json-parser.git
```

# Basic Usage


## From JSON to object

### Natural dict object
```python
from json_parser import interface_decoder
string = """{"a": "b", "c":"d"}"""
obj = interface_decoder.from_json(string)
````

### Custom class decoder
```python
from json_parser import IngredientsJsonDecoder
from json_parser import Candy
candy_json = """
        {
            "price" : 3.14,
            "ingredients" : [
                {
                    "naturalIngredients" : [
                        {
                            "name" : "rice syrup"
                        },
                        {
                            "name" : "honey"
                        }
                    ],
                    "artificialIngredients" : [
                        {
                            "name" : "food color"
                        },
                        {
                            "name" : "Monosodium Glutamate"
                        }
                    ]
                }
        
            ]
        }
"""
ingredients_decoder = IngredientsJsonDecoder()
candy_object = Candy.from_json(candy_json, ingredients_decoder)
```
