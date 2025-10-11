from dataclasses import dataclass
from datetime import date
from typing import Optional

from .document import Document

@dataclass(frozen=True) #deliniates immutability for this class
class PresidentialDocument(Document):
    presidental_document_number: int
    proclamation_number: int
    president: str
    signing_date: Optional[date]

    subtype: Optional[str]
    document_type: Optional[str] #the unique type of presidental documents
    