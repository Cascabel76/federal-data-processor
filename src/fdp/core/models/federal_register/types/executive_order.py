from presidential_document import PresidentialDocument
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ExecutiveOrder(PresidentialDocument): #this is a child class of the agnostic 'document' class
    eo_notes: Optional[str] 
    eo_number: Optional[str]
    amends_eos: List[str]
    revokes_eops: List[str]
