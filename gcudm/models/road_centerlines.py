#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/5/18
"""
.. currentmodule:: road_centerlines
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Say something descriptive about the 'road_centerlines' module.
"""

from ..meta import column, ColumnMeta, Requirement, Usage
from ..base import Base, EntityMixin
from sqlalchemy import Column, Integer, String, DateTime
from geoalchemy2 import Geometry


class RoadCenterline(Base, EntityMixin):

    __tablename__ = 'road_centerlines'

    geom = Column(Geometry('LINESTRING'))

    src_unq_id = column(
        String,
        ColumnMeta(
            label='NENA ID',
            nena='RCL_NGUID',
            requirement=Requirement.REQUESTED
        )
    )

    src_full_name = column(
        String,
        ColumnMeta(
            label='Source Full Name',
            requirement=Requirement.REQUESTED
        )
    )

    add_rng_pre_l = column(
        String,
        ColumnMeta(
            label='Left Address Number Prefix',
            requirement=Requirement.REQUESTED,
            nena='AdNumPre_L',
            usage=Usage.DISPLAY

        )
    )

    add_rng_pre_r = column(
        String,
        ColumnMeta(
            label='Right Address Number Prefix',
            requirement=Requirement.REQUESTED,
            nena='AdNumPre_R',
            usage=Usage.DISPLAY

        )
    )

    from_add_l = column(
        String,
        ColumnMeta(
            label="Left 'From' Address",
            nena='FromAddr_L',
            requirement=Requirement.REQUESTED,
            usage=Usage.DISPLAY
        )
    )

    to_add_l = column(
        String,
        ColumnMeta(
            label="Left 'To' Address",
            nena='ToAddr_L',
            requirement=Requirement.REQUESTED,
            usage=Usage.DISPLAY
        )
    )

    from_add_r = column(
        String,
        ColumnMeta(
            label="Right 'From' Address",
            nena='FromAddr_R',
            requirement=Requirement.REQUESTED,
            usage=Usage.DISPLAY
        )
    )

    to_add_r = column(
        String,
        ColumnMeta(
            label="Right 'To' Address",
            nena='ToAddr_R',
            requirement=Requirement.REQUESTED,
            usage=Usage.DISPLAY
        )
    )

    rng_type = column(
        String,
        ColumnMeta(
            label="Ranging Type"
        )
    )

    parity_l = column(
        String,
        ColumnMeta(
            label="Parity Left",
            nena="Parity_L"
        )
    )

    parity_r = column(
        String,
        ColumnMeta(
            label="Parity Right",
            nena="Parity_R"
        )
    )


