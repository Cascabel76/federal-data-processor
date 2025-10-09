from presidential_document import PresidentialDocument
from dataclasses import dataclass


@dataclass
class ExecutiveOrder(PresidentialDocument): #this is a child class of the agnostic 'document' class
    eo_notes: str 
    eo_number: int
