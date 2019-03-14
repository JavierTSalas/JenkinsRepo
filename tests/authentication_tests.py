#!/usr/bin/env python
"""Unit tests for the project1.authentication module."""

from unittest import TestCase
from mock import patch
import project1.authentication as auth

class StandAloneTests(TestCase):
    """Test the stand-alone module functions."""

    @patch('builtins.open')
    def test_login_success(self, mock_open):
        """Test the login function when things go right."""
        mock_open.return_value.read.return_value = "george|bosco"
        self.assertTrue(auth.login('george', 'bosco'))

    @patch('builtins.open')
    def test_login_bad_creds(self, mock_open):
        """Test the login function when bad creds are passed."""
        mock_open.return_value.read.return_value = "george|bosco"
        self.assertFalse(auth.login('george', 'marbleRye'))

    @patch('builtins.open')
    def test_login_error(self, mock_open):
        """Test the login function when an error happens."""
        mock_open.side_effect = IOError()
        self.assertFalse(auth.login('george', 'bosco'))

