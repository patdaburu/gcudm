#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/8/18
"""
.. currentmodule:: esbs
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module provides a common mixin for all emergency service boundary
object-relational model classes.
"""

from sqlalchemy import Column, String
from geoalchemy2 import Geometry
from ..meta import column, ColumnMeta, Requirement, Source, Target, Usage


class EsbMixin(object):
    """
    This mixin defines common attributes of emergency service boundary
    object-relational model classes.
    """
    geometry = Column(Geometry('POLYGON'))

    country = column(
        String,
        ColumnMeta(
            label='Country'
        )
    )

    state = column(
        String,
        ColumnMeta(
            label='State',
            target=Target(guaranteed=True)
        )
    )

    county = column(
        String,
        ColumnMeta(
            label='County'
        )
    )

    agencyID = column(
        String,
        ColumnMeta(
            label='Agency ID',
            nena='Agency_ID',
            source=Source(requirement=Requirement.REQUIRED),
            target=Target(guaranteed=True)
        )
    )

    routeURI = column(
        String,
        ColumnMeta(
            label='Service URI',
            nena='ServiceURI',
            source=Source(requirement=Requirement.REQUIRED),
            target=Target(guaranteed=True)
        )
    )

    serviceURN = column(
        String,
        ColumnMeta(
            label='Service URI',
            nena='ServiceURI',
            source=Source(requirement=Requirement.REQUIRED),
            target=Target(guaranteed=True)
        )
    )

    serviceNum = column(
        String,
        ColumnMeta(
            label='Service Number',
            nena='ServiceNum',
            target=Target(usage=Usage.DISPLAY)
        )
    )

    vCardURI = column(
        String,
        ColumnMeta(
            label='Agency vCard URI',
            nena='AVcard_URI'
        )
    )

    displayName = column(
        String,
        ColumnMeta(
            label='Display Name',
            nena='DisplayName',
            source=Source(requirement=Requirement.REQUIRED)
        )
    )
