#!/usr/bin/python
#-*- coding: utf-8 -*-

class Transaction:
    """A data class that stores transaction details."""
    def __init__(self):
        self.id = None
        self.startTime = None
        self.endTime = None
        self.bookDuration = None
        self.startOdometer = None
        self.endOdometer = None
        self.amount = None
        self.additionalFee = 0
        self.isPaid = None

