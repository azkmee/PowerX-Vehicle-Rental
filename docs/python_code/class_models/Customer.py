#!/usr/bin/python
#-*- coding: utf-8 -*-

from User import User

class Customer(User):
    def __init__(self):
        self.wallet = None

    def useVoucher(self, voucher):
        pass

    def viewAvailableVehicles(self, ):
        pass

    def rentVehicle(self, vehicle, transaction):
        pass

    def returnVehicle(self, vehicle, transaction):
        pass

    def makePayment(self, amount):
        pass

    def topupWallet(self, amount):
        pass

