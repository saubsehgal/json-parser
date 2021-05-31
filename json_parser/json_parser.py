import simdjson
from typing import List, Any, Type, Dict, Union
from datetime import date, datetime

KeyToClassMap = Dict[str, Type[Any]]
JSONPrimitive = Union[Dict[str, 'JSONPrimitive'], List['JSONPrimitive'], int, float, None, str, bool]


class JsonError(Exception):
    pass


class ClassMapLookUpFailError(JsonError):
    pass


class InterfaceDecoder:
    """
    Interface for decoding json. Custom Implementation can be done depending on the structure.
    A default json dict implementation has been provided.
    """
    def __init__(self,
                 class_map: KeyToClassMap = None,
                 type_key: str = '__type__',
                 data_key: str = '__data__',
                 treat_dict_as_ordered_dict: bool = True):
        """

        Args:
            class_map (ClassMap): Dictionary from string to Class
            type_key (str): Optional Default '__type__'.
            data_key (str): Optional Default '__data__'.
            treat_dict_as_ordered_dict (bool): Optional. Default True.
                treat all dictionary as ordered dict(python 3.6)
        """
        self.class_map = class_map
        self.type_key = type_key
        self.data_key = data_key
        self.treat_dict_as_ordered_dict = treat_dict_as_ordered_dict

    def from_json_dict(self, d: JSONPrimitive) -> Any:
        """Build an object from dictionary
        This is the place to override if you want to add custom class.

        Args:
            d (JSONPrimitive): JSONPrimitive. Ex: dict.

        Returns:
            Any
        """
        return self.default_from_json_dict(d)

    def from_json(self, s: str, **kwd) -> Any:
        """ Build object from  string.

        Args:
            s (str): json string
            **kwd (): The rest of keyword arguments will be passed down to json.loads

        Returns:
            Any. Object constructed from json string.
        """
        d = simdjson.loads(s, **kwd)
        return self.from_json_dict(d)

    def default_from_json_dict(self, json_data: JSONPrimitive) -> Any:
        """Default from json dictionary. Useful in fallback

        Args:
            json_data (JSONPrimitive): JSONPrimitive. Ex: dict.

        Returns:
            Any. Constructed Object.

        """
        type_key = self.type_key
        data_key = self.data_key

        if isinstance(json_data, dict):
            if type_key not in json_data:
                # assume string key dict
                return {k: self.from_json_dict(v) for k, v in json_data.items()}
            elif json_data[type_key] in self.class_map:
                obj_class = self.class_map[json_data[type_key]]
                if issubclass(obj_class, FromJson):
                    return obj_class.from_json_dict(json_data, decoder=self)
            elif json_data[type_key] == 'dict':
                data = json_data[data_key]
                return {self.from_json_dict(item['key']): self.from_json_dict(item['value']) for
                        item in data}
            elif json_data[type_key] == 'tuple':
                data = json_data[data_key]
                return tuple([self.from_json_dict(item) for item in data])
            elif json_data[type_key] == 'date':
                return date(**{k: v for k, v in json_data.items() if k != self.type_key})
            elif json_data[type_key] == 'datetime':
                return datetime(**{k: v for k, v in json_data.items() if k != self.type_key})
            elif json_data[type_key] == 'set':
                data = json_data[data_key]
                return set(data)
            elif json_data[type_key] == 'float':
                data = json_data[data_key]
                return float(data)
            else:
                raise ClassMapLookUpFailError('Failed to find type for k %r %r' % (json_data[type_key], json_data))
        elif isinstance(json_data, list):
            return [self.from_json_dict(item) for item in json_data]
        elif isinstance(json_data, (int, str, float)):
            return json_data
        elif json_data is None:
            return json_data
        else:
            raise NotImplementedError('Failed to parse json data %s, %r' % (type(json_data), json_data))


class IngredientsJsonDecoder(InterfaceDecoder):

    def from_json_dict(self, d: JSONPrimitive) -> Any:
        """Construct Ingredients from list of natural and artificial ingredients
        This is the place to override if you want to add custom class.

        Args:
            d (JSONPrimitive): JSONPrimitive. Ex: dict.

        Returns:
            Any
        """
        if self.class_map is None:
            self.class_map = {'naturalIngredients': NaturalIngredient, 'artificialIngredients': ArtificialIngredient}

        ingredients = []
        for dic in d:
            for key in dic:
                if key in self.class_map:
                    ingredients += list(map(self.class_map[key].from_json_dict, dic[key]))

        return ingredients


"""
Default decoder
"""
interface_decoder = InterfaceDecoder(class_map={})


class FromJson:
    """
    Interface for class that can be constructed from json
    """

    @classmethod
    def from_json_dict(cls, d: Dict[str, JSONPrimitive], decoder: InterfaceDecoder):
        """
        Construct object from dict
        Args:
            d (Dict[str, JSONPrimitive]): json dict
            decoder (InterfaceDecoder): decoder

        Returns:
            Object of this class.
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def from_json(cls, s: str, decoder: InterfaceDecoder = interface_decoder, **kwd):
        """Construct object from json string

        Args:
            s (str): json str
            decoder (InterfaceDecoder):
            **kwd (): the rest of keyword arguments are passed down to json.loads

        Returns:
            Object of this class.

        """
        d = simdjson.loads(s, **kwd)
        return cls.from_json_dict(d, decoder)


class ClassMap:
    @classmethod
    def construct_key_to_class_map(cls, class_list: List[Type[Any]]) -> KeyToClassMap:
        """Constructs a map containing key to class mapping from list of class
        Args:
            class_list (List[Type[Any]]): list of classes

        Returns:
            KeyToClassMap
        """
        return {cls.__name__: cls for cls in class_list}


class Ingredients(FromJson):
    def __init__(self, name: str):
        self.name = name

    @classmethod
    def from_json_dict(cls, ingredient_dict):
        """Construct object depending upon the Class of ingredient

                Args:
                    ingredient_dict: json dict
                Returns:
                    Object of Ingredient type.
                """
        return cls(**ingredient_dict)


class NaturalIngredient(Ingredients):
    """
    Type of Ingredient
    """
    def __init__(self, name: str):
        super().__init__(name)


class ArtificialIngredient(Ingredients):
    """
    Type of Ingredient
    """
    def __init__(self, name: str):
        super().__init__(name)


class Candy(FromJson):
    """
    Object Class to which Json needs to be converted
    """
    def __init__(self, price: float, ingredients: List[Ingredients]):
        self.price = price
        self.ingredients = ingredients

    @classmethod
    def from_json_dict(cls, json_data: Dict[str, JSONPrimitive], ingredients_json_decoder: IngredientsJsonDecoder):
        ingredients = ingredients_json_decoder.from_json_dict(json_data["ingredients"])
        return cls(json_data["price"], ingredients)
