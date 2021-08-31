#!/usr/bin/python
#-*- coding: utf-8 -*-

class Demerit:
    """A data class that stores demerit details."""
    def __init__(self):
        self.id = None
        self.transactionId = None
        self.customerId = None
        self.demeritDate = None
        self.description = None
        self.points = None
        self.isActive = None

