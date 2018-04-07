#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/4/18
"""
.. currentmodule:: base
.. moduleauthor:: Pat Daburu <pat@daburu.net>

The GeoAlchemy declarative base is defined in this module.
"""
from .meta import column, ColumnMeta, Requirement, Usage
from .types import GUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, DateTime


Base = declarative_base()  #: the declarative base class for the model


class ModelMixin(object):
    """
    This is the parent class for all entity classes in the model.  It defines
    common fields.
    """
    gcUnqId = column(
        GUID,
        meta=ColumnMeta(
            label='GeoComm ID',
            guaranteed=True,
            calculated=True
        ),
        primary_key=True
    )

    srcOfData = column(
        String,
        ColumnMeta(
            label='Data Source'
        )
    )

    srcLastEd = column(
        DateTime,
        ColumnMeta(
            label='Source of Last Update'
        )
    )

    uploadAuth = column(
        String,
        ColumnMeta(
            label='Upload Authority'
        )
    )

    updateDate = column(
        DateTime,
        ColumnMeta(
            label='Last Update'
        )
    )

    effective = column(
        DateTime,
        ColumnMeta(
            label='Effective Date',
            requirement=Requirement.REQUESTED
        )
    )

    expire = column(
        DateTime,
        ColumnMeta(
            label='Expiration Date',
            requirement=Requirement.REQUESTED
        )
    )

    @staticmethod
    def get_geometry_type():
        return 'LINESTRING'  # TODO: Retrieve the geometry type.

