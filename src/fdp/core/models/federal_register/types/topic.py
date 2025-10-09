from dataclasses import dataclass

@dataclass
class Topic:
    ''' This is an often unused aspect of the federal register, but included to prevent missed data points. This is a string of topics from the JSON file'''
    name: str