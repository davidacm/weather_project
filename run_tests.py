#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os

test_directory = "unitTests"

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_directory, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
