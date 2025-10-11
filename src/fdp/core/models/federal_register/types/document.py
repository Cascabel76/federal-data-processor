#this is a base document dataclass that is meant to be agnostic to documents.
from dataclasses import dataclass, field
from datetime import date, datetime #Always store UTC with ISO 8601; never trust API timezone docs—normalize on ingest.
from typing import Optional, Dict, List

#importing sub-dataclasses from the typing models
from .agency import Agency
from .topic import Topic
from .attachment import Attachment

@dataclass(frozen=True, slots=True, kw_only=True)
class Document:
    '''agnostic class for recording federal register documents'''
    #these are listed in a somewhat alphabetical order
    abstract: Optional[str] = None
    action: Optional[str] = None
    agencies: List[Agency] = field(default_factory=list)
    attachments: List[Attachment] = field(default_factory=list)
    comment_url: Optional[str] = None
    citation: Optional[str] = None
    dates: Optional[str] = None #this is a strange one, but we can work around this I think it appears to mention dates that they will be meeting reagarding this matter.+
    disposition_notes: Optional[str] = None
    doc_ids: List[str] #this should be the main key for the objects created in this data class, it will map to C extensions later in development.
    doc_type: str #might be worth changing to enum later on -> would allow for more complex data relationships
    docket_id: List[str] = field(default_factory=list)
    effective_date: Optional[date] = None
    html_url: str
    is_withdrawn: bool = False
    is_amendment: bool = False
    last_modified: datetime #convert to utc timezone at ingest for utc formatting
    publication_date: date
    pdf_url: Optional[str] = None
    provenance: Dict[str, str] = field(default_factory=dict)#records, timestamps, hash this is just meta data
    raw_hash: Optional[str] = None #hash of raw payload
    topics: List[Topic] = field(default_factory=list)# a list of the topics that are meta-data for documents on the federal register.
    title: str
    