# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function

from marshmallow import fields, missing, Schema


# noinspection PyUnusedLocal
def get_id(obj, context):
    """Get record id."""
    pid = context.get('pid')
    return pid.pid_value if pid else missing


class InvenioRecordSchemaV1Mixin(Schema):
    """Invenio record"""

    id = fields.Function(
        serialize=get_id,
        deserialize=get_id)
