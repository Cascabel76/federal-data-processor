#this is a pythong dataclass written by Enrique Castro
from dataclasses import dataclass


@dataclass
class Agency:
    agency_raw_name: str
    agency_name: str
    agency_id: int
    agency_url: str
    agency_json_url: str
    agency_parent_id: int
    agency_slug: str