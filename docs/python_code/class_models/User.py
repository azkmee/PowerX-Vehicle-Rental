#!/usr/bin/python
#-*- coding: utf-8 -*-

class User:
    """A data class that stores customer/admin details."""
    def __init__(self):
        self.id = None
        self.fullName = None
        self.dob = None
        self.email = None
        self.mobile = None
        self.address = None
        self.isActive = None

    def registerSelf(self, new):
        pass

    def editSelf(self, id, new):
        pass

