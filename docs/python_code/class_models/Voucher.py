#!/usr/bin/python
#-*- coding: utf-8 -*-

class Voucher:
    """A data class that stores voucher details."""
    def __init__(self):
        self.id = None
        self.customerId = None
        self.transactionId = None
        self.discount = None
        self.issueDate = None
        self.expDate = None

