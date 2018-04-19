#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/4/18
"""
.. currentmodule:: base
.. moduleauthor:: Pat Daburu <pat@daburu.net>

The GeoAlchemy declarative base for the data model is defined in this module
along with some other helpful classes.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, DateTime
from .geometry import GeometryTypes
from .meta import column, ColumnMeta, Requirement
from .types import GUID


Base = declarative_base()  #: This is the model's declarative base.  pylint: disable=invalid-name


class ModelMixin(object):
    """
    This mixin includes columns and methods common to objects within the
    data model.
    """
    __geoattr__ = 'geometry'  #: the name of the geometry column attribute

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

    srcUnqId = column(
        String,
        ColumnMeta(
            label='NENA ID',
            nena='RCL_NGUID',
            requirement=Requirement.REQUESTED
        )
    )

    @classmethod
    def geometry_type(cls) -> GeometryTypes:
        """
        Get the geometry type defined for the model class.

        :return: the geometry type
        """
        try:
            # Get the string that identifies the geometry type.
            gt_str = cls.__table__.c[cls.__geoattr__].type.geometry_type
            # The string should correspond to one of the supported types.
            gtyp = GeometryTypes[gt_str]
            # Return that value.
            return gtyp
        except KeyError:
            return GeometryTypes.NONE
