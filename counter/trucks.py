# Stalmic Distributors Inventory Count Project
# Created by Aaron Daughtry, December 12, 2016
#
# Truck-related classes, mostly to use with reports from bMobile.

# Python 2 and 3 compatibility.
from __future__ import print_function
from builtins import input

import csv
from datetime import *
import os
# The date format.
from count import D_FORMAT


class TruckInvoices:
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
            if (inv[30] != 0) and (inv[0:28] != reader[i][0:28]):
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

    def query(self, route, date):
        """
        Query a route on a specific date and return all items sold on that
        route.
        """
        if route not in self.invoices_r.keys():
            print("There are no invoices for the specified route.")
        else:
            try: 
                datetime.strptime(date, D_FORMAT)
            except ValueError:
                print("Date is not in a valid format (MM/DD/YYYY).")
            else:
                return [x for x in self.invoices_r[route] if x[0] == date]


class TruckLoads:
    """
    An object containing all truck loads, grouped either by route or truck.
    Similar to TruckInvoices.
    """
    def __init__(self, filelist):
        self.loads = []
        self.loads_r = {}
        self.loads_t = {}
        # Unlike the truck invoices, the truck loads rest in many different
        # files (they cannot be sourced from the same report that we source
        # invoices from because of wackiness with the same load being listed
        # twice for different invoices. Therfore, pass this item an array of
        # files.)
        for filename in filelist:
            with open(filename, newline='', encoding='utf-8-sig') as file:
                reader = list(csv.reader(file))
            date = os.path.basename(filename)[:-4]
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
                date = date.strftime(D_FORMAT)
            except ValueError:
                print("Load file not named correctly.", end=" ")
                print("Filenames must be a date in the form YYYY-MM-DD.")
            for i, load in enumerate(reader):
                try:
                    if load[5]:
                        load[5] = float(load[5].replace(',', ''))
                    else:
                        load[5] = 0
                except ValueError:
                    print("There was an error at location", end=" ")
                    print("%s, 5 (%s)." % (i, load[5]), end=" ")
                    print("Value must be a number.")
                    load[5] = 0
                # Make the truck case insensitive.
                load[1] = load[1].lower().replace(' ', '')
                if load[0] != '':
                    data = [0, 1, 2, 5]
                    self.loads.append([date] + [load[x] for x in data])
                    if load[0] not in self.loads_r.keys():
                        self.loads_r[load[0]] = []
                    data = [1, 2, 5]
                    self.loads_r[load[0]].append([date]+[load[x] for x in data])
                    if load[1] not in self.loads_t.keys():
                        self.loads_t[load[1]] = []
                    data = [0, 2, 5]
                    self.loads_t[load[1]].append([date]+[load[x] for x in data])

    def query(self, truck, date):
        if truck not in self.loads_t.keys():
            print("There are no loads for that truck.")
        else:
            try:
                datetime.strptime(date, D_FORMAT)
            except ValueError:
                print("Date is not in a valid format (MM/DD/YYYY).")
            else:
                return [x for x in self.loads_t[truck] if x[0] == date]
