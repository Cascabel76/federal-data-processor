from document import Document
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class PresidentialDocument(Document):
    presidental_doc_num: int
    prcolamation_number: int
    president: str
    signing_date: Optional[date]

# UNSURE OF THESE
    subtype: str
    type: str