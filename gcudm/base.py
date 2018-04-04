#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/4/18
"""
.. currentmodule:: base
.. moduleauthor:: Pat Daburu <pat@daburu.net>

The GeoAlchemy declarative base is defined in this module.
"""
from .meta import column, ColumnMeta
from .types import GUID
from abc import ABCMeta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from geoalchemy2 import Geometry

Base = declarative_base()  #: the declarative base class


class EntityMixin(object):
    """
    This is the parent class for all entity classes in the model.
    """
    gc_unq_id = column(
        GUID,
        meta=ColumnMeta(
            friendly='GeoComm ID'
        ),
        primary_key=True
    )
    src_of_data = column(
        String,
        ColumnMeta(
            friendly='Data Source'
        )
    )
    src_last_ed = column(
        DateTime,
        ColumnMeta(
            friendly='Source of Last Update'
        )
    )
    upload_auth = column(
        String,
        ColumnMeta(
            friendly='Upload Authority'
        )
    )
    update_date = column(
        DateTime,
        ColumnMeta(
            friendly='Last Update'
        )
    )
    effective = column(
        DateTime,
        ColumnMeta(
            friendly='Effective Date'
        )
    )
    expire = column(
        DateTime,
        ColumnMeta(
            friendly='Expiration Date'
        )
    )


