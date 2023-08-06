#!/usr/bin/env python3

"""
(C) 2019 Damir Cavar, Oren Baldinger, Maanvitha Gongalla, Anurag Kumar, Murali Kammili

Functions for manipulating and expanding a JSON-NLP object

Licensed under the Apache License 2.0, see the file LICENSE for more details.

Brought to you by the NLP-Lab.org (https://nlp-lab.org/)!
"""
import datetime
from collections import OrderedDict
from typing import List

name = "pyjsonnlp"
__version__ = "0.2.33"


def get_base() -> OrderedDict:
    """
    Return a base framework for JSON-NLP.
    :returns Base frame for a JSON-NLP object
    :rtype OrderedDict
    """

    return OrderedDict({
        "meta": {
            "DC.conformsTo": __version__,
            "DC.source": "",  # where did the corpus come from
            "DC.created": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "DC.date": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "DC.creator": "",
            'DC.publisher': "",
            "DC.title": "",
            "DC.description": "",
            "DC.identifier": "",
            "DC.language": "",
            "DC.subject": "",
            "DC.contributors": "",
            "DC.type": "",
            "DC.format": "",
            "DC.relation": "",
            "DC.coverage": "",
            "DC.rights": "",
            "counts": {},
        },
        "conll": {},
        #"documents": {}
        "documents": []
    })


def get_base_document(doc_id: int) -> OrderedDict:
    """Returns a JSON base document."""

    return OrderedDict({
        "meta": {
            "DC.conformsTo": __version__,
            "DC.source": "",  # where did the corpus come from
            "DC.created": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "DC.date": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "DC.creator": "",
            'DC.publisher': "",
            "DC.title": "",
            "DC.description": "",
            "DC.identifier": "",
            "DC.language": "",
            "DC.subject": "",
            "DC.contributors": "",
            "DC.type": "",
            "DC.format": "",
            "DC.relation": "",
            "DC.coverage": "",
            "DC.rights": "",
            "counts": {},
        },
        "id": doc_id,
        "conllId": "",
        "text": "",
        "tokenList": [],
        #"clauses": {},
        "sentences": {},
        "paragraphs": {},
        "dependencies": [],
        "coreferences": [],
        "constituents": [],
        "expressions": [],
    })


def remove_empty_fields(json_nlp: OrderedDict) -> OrderedDict:
    """Remove empty fields from root, meta, and documents"""
    cleaned = OrderedDict()
    for k, v in json_nlp.items():
        if v != '' and v != [] and v != {}:
            cleaned[k] = v
    if 'meta' in cleaned:
        cleaned['meta'] = remove_empty_fields(cleaned['meta'])
    if 'documents' in cleaned:
        #for i, d in cleaned['documents'].items():
        for i in range(len(cleaned['documents'])):
            cleaned['documents'][i] = remove_empty_fields(cleaned['documents'][i])
    return cleaned


def find_head(doc: OrderedDict, token_ids: List[int], sentence_id: int, style='universal') -> int:
    """
    Given phrase, clause, or other group of token ids, use a dependency parse to find the head token.
    We create two sets, governors and dependents of the tokens in token_ids. The elements in gov that do not occur
    in dependents are the heads. There should be just one.
    """
    #print(sentence_id, doc['dependencies'],doc['dependencies']['trees'])
    if len(token_ids) == 0:
        return None
    arcs = doc['dependencies'][sentence_id-1]['trees']
    govs = set(token_ids)
    for x in arcs:
        if x["dep"] in govs and x["gov"] in govs:
            govs.remove(x["dep"])
    govs = list(govs)
    if len(govs) == 0:
        return None
    return govs[0]



def build_coreference(reference_id: int) -> dict:
    """Build a frame for a coreference structure"""

    return {
        'id': reference_id,
        'representative': {
            'tokens': []
        },
        'referents': []
    }


def build_constituents(sent_id: int, s: str) -> dict:
    """ """
    s = s.rstrip().lstrip()
    open_bracket = s[0]  # ( or [
    close_bracket = s[-1]  # ) or ]
    return {
        'sentenceId': sent_id,
        'labeledBracketing': f'{open_bracket}ROOT {s}{close_bracket}' if s[1:5] != 'ROOT' else s
    }
