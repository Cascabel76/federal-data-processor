#this is a base document dataclass that is meant to be agnotisc to documents.
from dataclasses import dataclass
from datetime import date, datetime #Always store UTC with ISO 8601; never trust API timezone docs—normalize on ingest.
from typing import Optional, Dict, List

#importing sub-dataclasses from the typing models
from agency import Agency
from topic import Topic
from attachment import Attachment

@dataclass
class Document:
    '''angostic class for recording federal register documents'''
    #these are listed in a somewhat alphabetical order
    abstract: Optional[str]
    action: str
    agencies: List[Agency] = None
    attachments: List[Attachment] = None
    comment_url: Optional[str]
    citations: str
    dates: str #this is a strange one, but we can work around this I think it appears to mention dates that they will be meeting reagarding this matter.+
    disposition_notes: Optional[str] = None
    doc_id: str #this should be the main key for the obejects created in this data class, it will map to C extensions later in development.
    doc_type: str #might be worth changing to enum later on -> would allow for more complex data relationships
    docket_id: Optional[str]
    effective_date: Optional[date]
    html_url: str
    is_widthdrawn: bool = False
    is_admendment: bool = False
    last_modified: datetime #convert to utc timezone at ingest for utc formatting
    publication_date: date
    pdf_url: Optional[str]
    provenance: Dict[str, str] = None #records, timestamps, hash this is just meta data
    raw_hash: Optional[str] = None #hash of raw paylaod
    topics: List[Topic] = None # a list of the topics that are meta-data for documents on the federal register.
    title: str