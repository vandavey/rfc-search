#!/usr/bin/env python3
#
#  rfc_spec.py
#  -----------
#  Source file for the RFC specification metadata class.
#
import json
from typing import Dict


class RfcSpec(object):
    """
    RFC specification entry metadata.
    """
    def __init__(self,
                 id: int = 0,
                 files: Dict[str, str] = None,
                 title: str = str(),
                 authors: str = str(),
                 date: str = str(),
                 more_info: str = str(),
                 status: str = str(),
                 txt_url: str = str(),
                 info_url: str = str()):
        """
        Initialize the object.
        """
        self.Id: int = id
        self.Files: Dict[str, str] = files if files else {}
        self.Title: str = title
        self.Authors: str = authors
        self.Date: str = date
        self.MoreInfo: str = more_info
        self.Status: str = status
        self.InfoUrl: str = info_url
        self.TxtUrl: str = txt_url

    def __repr__(self) -> str:
        """
        Get the string representation of the specification.
        """
        return f'"rfc{self.Id}": {self.json()}'

    def json(self, indent: int = 4) -> str:
        """
        Get the RFC specification as a JSON string.
        """
        return json.dumps(self.__dict__, indent=abs(indent))
