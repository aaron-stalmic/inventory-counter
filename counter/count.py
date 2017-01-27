# Stalmic Distributors Inventory Count Project
# Created by Aaron Daughtry, December 12, 2016
#
# Count class for count objects. Stores info on counts as well as methods for
# querying, editing, and outputting count information.

# Python 2 and 3 compatibility.
from __future__ import print_function
from builtins import input

import csv
from datetime import *

D_FORMAT = '%m/%d/%Y'


class Count:
    """
    An inventory count generated from a CSV. Data should be listed with items
    along the leftmost column and dates of counts along the top. Class is a
    dictionary with the item name returning an array of counts.
    """

    def __init__(self, filename):
        self.count = {}
        # Excel automatically outputs CSV files with a byte order mark at the
        # beginning of the file, so we need to import with the utf-8-sig
        # encoding.
        with open(filename, newline='', encoding='utf-8-sig') as file:
            reader = list(csv.reader(file))
            # The start date will be the first date listed in the count.
            self.start = datetime.strptime(reader[0][1], D_FORMAT)
            self.length = 0
            for i, row in enumerate(reader[1:]):
                # Find the length of the longest row, not including the item.
                if len(row) > self.length:
                    self.length = len(row) - 1
                # Convert item quantities to floats for manipulating.
                for j, item in enumerate(row[1:]):
                    try:
                        if item:
                            row[j+1] = float(item)
                        else:
                            row[j+1] = 0
                    except ValueError:
                        print("There was an error at location", end=" ")
                        print("%s, %s (%s)." % (i, j, item), end=" ")
                        print("Value must be a number.")
                        row[j+1] = 0
                # There have been items in the past with quote marks that mess
                # up the CSV files.
                self.count[row[0].strip('"')] = row[1:]

    def query(self, item, date):
        """
        Query the count by item and date.
        """
        try:
            date = datetime.strptime(date, D_FORMAT)
        except ValueError:
            print("Date is not in a valid format (MM/DD/YYYY).")
        try:
            return self.count[item][(date - self.start).days]
        except KeyError:
            print("Item does not exist in count.")
        except IndexError:
            print("Date is not in count.")

    def start_date(self, item, format=True):
        """
        Returns the start date for an item, and none if an item has not been
        counted.
        """
        try:
            i = next((i for i, x in enumerate(self.count[item]) if x), None)
        except KeyError:
            print("Item does not exist in count.")
        if i is None:
            return None
        else:
            if format:
                return (self.start + timedelta(i)).strftime(D_FORMAT)
            else:
                return self.start + timedelta(i)

    def edit(self, item, date, amt):
        """
        Edit an item.
        """
        if type(date) != datetime.datetime:
            try:
                date = datetime.strptime(date, D_FORMAT)
        try:
            index = (date - self.start).days
        try:
            self.count[item][index] += amt
        except KeyError:
            print("Item does not exist in count.")
        except IndexError:
            print("Date is not in count.")
        except TypeError:
            print("Value must be a number.")

    def output(self, filename):
        """
        Outputs the count to a CSV file.
        """
        total = 0
        with open(filename, 'w+') as file:
            file.write('="Item"')
            # So that we don't have to iterate through the count twice to get
            # a total sum, this space is left for the sum later. Therefore, the
            # maximum number of inventory items supported is 9,999,999,999. :^)
            file.write(',            ')
            for i in range(0, self.length):
                date = (self.start + timedelta(i)).strftime(D_FORMAT)
                file.write(', %s' % date)
            for item in sorted(self.count.keys()):
                file.write('\n="%s"' % item)
                item_sum = sum(self.count[item])
                total += item_sum
                file.write(', %s' % str(item_sum))
                for qty in self.count[item]:
                    file.write(', %s' % qty)
            file.seek(8)
            file.write(str(total))
