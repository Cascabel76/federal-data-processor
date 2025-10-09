
from dataclasses import dataclass
from document import Document

@dataclass
class Notice(Document): #this is a child object that inherits the varibles of the agnostics document class
    action: str
    