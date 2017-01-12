# Stalmic Distributors Inventory Count Project
# Created by Aaron Daughtry, December 12, 2016
#
# Truck-related classes, mostly to use with reports from bMobile.

# Python 2 and 3 compatibility.
from __future__ import print_function
from builtins import input

import csv


class TruckInvoice:
    """
    An object containing all truck invoices for all trucks, grouped either by
    route or truck.
    """

    def __init__(self, filename):
        # Three separate listing methods: A list with no sorting at all, a
        # dictionary grouped by route, and a dictionary grouped by truck.
        self.invoices = []
        self.invoices_r = {}
        self.invoices_t = {}
        with open(filename, newline='', encoding='utf-8-sig') as file:
            reader = list(csv.reader(file))
            # The default list from bMobile has several instances of repetition
            # and 0 values that are not required in the final list. This
            # algorithm picks out the first unique value ONLY in a sequence.
            # This data is taken from the bMobile Route Balance Variance
            # Report, and the relevant data is in columns 21, 18, 20, 27, & 30
            # (Date, Route, Truck, Item, and Amt Sold)
            # An extra item is added to the beginning of reader to help with
            # iteration.
            reader = [[0]*40] + reader
            for i, inv in enumerate(reader[1:]):
                if (inv[0:28] != reader[i][0:28] and
                   inv[30] not in ['0', '0.00']):
                    try:
                        if inv[30]:
                            # bMobile puts commas in numbers greater than 1000,
                            # which will throw an error if we try to convert
                            # them to floats. So strip out the commas.
                            inv[30] = float(inv[30].replace(',', ''))
                        else:
                            inv[30] = 0
                    except ValueError:
                        print("There was an error at location", end=" ")
                        print("%s, 30 (%s)." % (i, inv[30]), end=" ")
                        print("Value must be a number.")
                        inv[30] = 0
                    # Make the truck case insensitive.
                    inv[20] = inv[20].lower().replace(' ', '')
                    # Pick out the relevant information and add it to our table
                    # and dictionaries.
                    if inv[30] != 0:
                        data = [21, 18, 20, 27, 30]
                        self.invoices.append([inv[x] for x in data])
                        if inv[18] not in self.invoices_r.keys():
                            self.invoices_r[inv[18]] = []
                        data = [21, 20, 27, 30]
                        self.invoices_r[inv[18]].append([inv[x] for x in data])
                        if inv[20] not in self.invoices_t.keys():
                            self.invoices_t[inv[20]] = []
                        data = [21, 18, 27, 30]
                        self.invoices_t[inv[20]].append([inv[x] for x in data])
