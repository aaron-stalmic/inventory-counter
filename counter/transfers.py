# Stalmic Distributors Inventory Count Project
# Created by Aaron Daughtry, December 12, 2016
#
# Transfer-related classes, mostly to use with reports from Quickbooks.

# Python 2 and 3 compatibility.
from __future__ import print_function
from builtins import input

import csv
from datetime import *
import os
# The date format.
from count import D_FORMAT


class Transfers:
    """
    An object containing a list of transfers.
    """

    def __init__(self, filename, trans_dict):
        # The transfers are sourced from a transaction report in Quickbooks.
        # They are structured as a bunch of item adjustments, usually in pairs.
        # So a transfer of an item negatively adjusts inventory from the source
        # and positively adjusts inventory at the receiving warehouse. This
        # means that there would only ever be one file to deal with, as all
        # warehouses will be listed in the transfer list.
        self.transfers = []
        # Warehouse invoices are in separate CSV files, named after their
        # location.
        with open(filename, newline='', encoding='utf-8-sig') as file:
            reader = list(csv.reader(file))
        try:
            reader = [x for x in reader if x[1] == 'Inventory Transfer']
        except IndexError:
            print("Something's wrong.", end=" ")
            print("Perhaps you did not generate the transfer file correctly?")
        for t, tran in enumerate(reader):
            # Inventory transfer entries are preceded by their type.
            try:
                if tran[7]:
                    tran[7] = float(tran[7].replace(',', ''))
                else:
                    tran[7] = 0
            except ValueError:
                print("There was an error at location", end=" ")
                print("%s, 7 (%s)." % (t, tran[7]), end=" ")
                print("Value must be a number.")
                tran[7] = 0
            tran[5] = tran[5].split(' (')[0]
            # Convert site to a key using the translation dictionary.
            try:
                tran[9] = trans_dict[tran[9]]
            except KeyError:
                print("Site %s" % tran[9], end=" ")
                print("was not found in the provided translation dictionary.")
            data = [3, 5, 7, 9]
            self.transfers.append([tran[x] for x in data])

    def query(self, date):
        """
        Queries for transfers on a specific date.
        """
        try:
            datetime.strptime(date, D_FORMAT)
        except ValueError:
            print("Date is not in a valid format (MM/DD/YYYY).")
        else:
            return [x for x in self.transfers if x[0] == date]
