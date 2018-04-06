#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/6/18

import unittest
import gcudm.model


class TestSuite(unittest.TestCase):

    def test_import_loadModel_succeeds(self):
        gcudm.model.load()
        self.assertEqual(True, True)

    def test_skipOnLoad_loadModel_succeeds(self):
        # Skip one model module to cover the condition.
        gcudm.model._SKIP_ON_LOAD.append('gcudm.models.road_centerlines')
        gcudm.model.load()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

