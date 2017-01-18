# Stalmic Distributors Inventory Count Project
# Created by Aaron Daughtry, December 12, 2016
#
# Warehouse-related classes, mostly to use with reports from Quickbooks.

# Python 2 and 3 compatibility.
from __future__ import print_function
from builtins import input

import csv
from datetime import *
import os
# The date format.
from count import D_FORMAT
# The prefixes on invoices for those that come from the warehouse, and not from
# a truck.
WH_PREFIXES = ['BH', 'MR', 'VN', 'KB']


class WarehouseInvoices:
    """
    An object containing all dictionaires of invoices, grouped by warehouse.
    """

    def __init__(self, filelist):
        # The invoices are sourced from Quickbooks, since bMobile does not
        # store any warehouse invoices. To generate the invoices, we use sales
        # by item detail, with only the columns item, number, date, and
        # quantity, which is then exported to excel and saved as a CSV.
        self.invoices = {}
        # Warehouse invoices are in separate CSV files, named after their
        # location.
        for filename in filelist:
            name = os.path.basename(filename)[:-4]
            self.invoices[name] = []
            with open(filename, newline='', encoding='utf-8-sig') as file:
                reader = list(csv.reader(file))
            for i, inv in enumerate(reader):
                try:
                    # Remove blank lines (begin with 3 blank cells) and any
                    # invoices that are not sourced from the warehouse.
                    if (len(inv) > 3 and
                       inv[0:3] == ['']*3 and
                       inv[5][0:2] in WH_PREFIXES):
                        try:
                            if inv[9]:
                                inv[9] = float(inv[9].replace(',', ''))
                            else:
                                inv[9] = 0
                        except ValueError:
                            print("There was an error at location", end=" ")
                            print("%s, 9 (%s)." % (i, inv[9]), end=" ")
                            print("Value must be a number.")
                            inv[9] = 0
                        inv[7] = inv[7].split(' (')[0]
                        data = [3, 5, 7, 9]
                        self.invoices[name].append([inv[x] for x in data])
                except IndexError:
                    print("Something's wrong.", end=" ")
                    print("Perhaps you did not generate the invoice file correctly?")

    def query(self, location, date):
        """
        Queries a location for invoices on a specific date and returns all
        items sold on that date.
        """
        if location not in self.invoices.keys():
            print("There are no invoices for that location.")
        else:
            try:
                datetime.strptime(date, D_FORMAT)
            except ValueError:
                print("Date is not in a valid format (MM/DD/YYYY).")
            else:
                return [x for x in self.invoices[location] if x[0] == date]


class WarehousePurchases:
    """
    An object containing all dictionaires of purchases, grouped by warehouse.
    """

    def __init__(self, filelist):
        self.purchases = {}
        for filename in filelist:
            name = os.path.basename(filename)[:-4]
            self.purchases[name] = []
            with open(filename, newline='', encoding='utf-8-sig') as file:
                reader = list(csv.reader(file))
            for p, pur in enumerate(reader):
                try:
                    if (len(pur) > 3 and
                       pur[0:3] == ['']*3):
                        try:
                            if pur[7]:
                                pur[7] = float(pur[7].replace(',', ''))
                            else:
                                pur[7] = 0
                        except ValueError:
                            print("There was an error at location", end=" ")
                            print("%s, 7 (%s)." % (p, pur[7]), end=" ")
                            print("Value must be a number.")
                            pur[7] = 0
                        pur[5] = pur[5].split(' (')[0]
                        data = [3, 5, 7]
                        self.purchases[name].append([pur[x] for x in data])
                except IndexError:
                    print("Something's wrong.", end=" ")
                    print("Perhaps you did not generate the invoice file correctly?")

    def query(self, location, date):
        """
        Queries a location for invoices on a specific date and returns all
        items sold on that date.
        """
        if location not in self.purchases.keys():
            print("There are no invoices for that location.")
        else:
            try:
                datetime.strptime(date, D_FORMAT)
            except ValueError:
                print("Date is not in a valid format (MM/DD/YYYY).")
            else:
                return [x for x in self.purchases[location] if x[0] == date]
