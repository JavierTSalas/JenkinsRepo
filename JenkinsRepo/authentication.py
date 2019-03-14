#!/usr/bin/env python
"""This module provides functions for authenticating users."""

def login(username, password):
    """Log the user in."""
    try:
        user_file = open('/etc/users.txt')    
        user_buf = user_file.read()
        users = [line.split("|") for line in user_buf.split("\n")]
        return [username, password] in users
    except IOError:
        print ("I can't authentication you.")
        return False

