#!/usr/bin/python
#-*- coding: utf-8 -*-

class VehicleRentalService:
    """A Service Layer class that implements all methods called by Customer or Admin."""
    def __init__(self):
        self.listTransactions = None
        self.listVehicles = None
        self.listVouchers = None
        self.listDemerit = None

