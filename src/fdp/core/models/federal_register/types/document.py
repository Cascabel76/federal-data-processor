#this is a base document dataclass that is meant to be agnotisc to documents.
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Dict, List

#importing sub-dataclasses from the typing models
from agency import Agency
from topic import Topic
from attachment import Attachment

@dataclass
class Document:
    '''angostic class for recording federal register documents'''
    doc_id: str
    doc_type: str #might be worth changing to enum later on -> would allow for more complex data relationships
    title: str
    abstract: Optional[str]
    publication_date: date
    effective_date: Optional[date]
    last_modified: datetime #convert to utc timezone at ingest for utc formatting
    html_url: str
    pdf_url: Optional[str]
    comment_url: Optional[str]
    docket_id: Optional[str]
    is_widthdrawn: bool = False
    is_admendment: bool = False
    eo_number: Optional[str] = None
    president: Optional[str] = None
    provenance: Dict[str, str] = None #records, timestamps, hash
    raw_hash: Optional[str] = None #hash of raw paylaod
    agencies: List[Agency] = None
    topics: List[Topic] = None
    attachments: List[Attachment] = None
