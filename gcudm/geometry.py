#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/14/18
"""
.. currentmodule:: geometry
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module contains stuff pertaining to geometry columns.
"""

from enum import IntFlag


class GeometryTypes(IntFlag):
    NONE = 0  #: no geometry type
    POINT = 1  #: point geometries
    LINESTRING = 2  #: polyline geometries
    POLYGON = 3  #: polygon geometries
