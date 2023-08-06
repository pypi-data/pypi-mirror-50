#!/bin/env python3

#######################################################################
# Copyright (C) 2019 David Palao
#
# This file is part of QULo.
#
#  QULo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  QULo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with QULo.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

import unittest
from unittest.mock import MagicMock, patch

import sys
from qulo.error_handling import CannotLog, handle_errors
from qulo.constants import START_STOP_ERROR


class CannotLogTestCase(unittest.TestCase):
    def test_is_exception(self):
        with self.assertRaises(CannotLog):
            raise CannotLog()

        
class handle_errorsTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_f = MagicMock()
        
    def test_calls_the_decorated_function(self):
        decorated_f = handle_errors(self.mock_f)
        args = (8, "se")
        kwargs = {"ke": "kieres", "WW": 3}
        decorated_f(*args, **kwargs)
        self.mock_f.assert_called_once_with(*args, **kwargs)

    def test_returns_result_from_function(self):
        result = "$$$%$L"
        self.mock_f.return_value=result
        decorated_f = handle_errors(self.mock_f)
        returned = decorated_f()
        self.assertEqual(result, returned)

    @patch("qulo.error_handling.print")
    def test_behaviour_on_PermissionError(self, pprint):
        msg = "bla bla"
        ex = CannotLog(msg)
        self.mock_f.side_effect=ex
        decorated_f = handle_errors(self.mock_f)
        with self.assertRaises(SystemExit) as e:
            decorated_f()
        print(e.exception.code)
        self.assertEqual(e.exception.code, START_STOP_ERROR)
        pprint.assert_called_once_with(msg, file=sys.stderr)

    def test_function_metadada_preserved(self):
        self.mock_f.__doc__ = "shf"
        decorated_f = handle_errors(self.mock_f)
        self.assertEqual(decorated_f.__doc__, "shf")
        
