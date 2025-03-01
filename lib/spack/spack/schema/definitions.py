# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for definitions

.. literalinclude:: _spack_root/lib/spack/spack/schema/definitions.py
   :lines: 16-
"""
from typing import Any, Dict

from .spec_list import spec_list_schema

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "definitions": {
        "type": "array",
        "default": [],
        "items": {
            "type": "object",
            "properties": {"when": {"type": "string"}},
            "additionalProperties": spec_list_schema,
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack definitions configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
