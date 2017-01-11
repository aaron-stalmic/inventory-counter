# Stalmic Distributors Inventory Count Project
# Created by Aaron Daughtry, December 12, 2016
#
# The purpose of this project is to take data in the form of count, invoice,
# truck load, and transfer data in CSV files (generated from Quickbooks and
# bMobile) and manipulate it to give final inventory figures.
#
# Please see the README file for other documentation.

# Python 2 and 3 compatibility.
from __future__ import print_function
from builtins import input

import csv
import os
from datetime import *


class count:
    """
    An inventory count generated from a CSV. Data should be listed with items
    along the leftmost column and dates of counts along the top. Class is a
    dictionary with the item name returning an array of counts.
    """
    D_FORMAT = '%m/%d/%Y'

    def __init__(self, filename):
        self.count = {}
        with open(filename, newline='', encoding='utf-8-sig') as file:
            reader = list(csv.reader(file))
            self.start = datetime.strptime(reader[0][1], self.D_FORMAT)
            self.length = 0
            for i, row in enumerate(reader[1:]):
                if len(row) > self.length:
                    self.length = len(row) - 1
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
            date = datetime.strptime(date, self.D_FORMAT)
        except ValueError:
            print("Date is not in a valid format (MM/DD/YYYY)")
        try:
            return self.count[item][(date - self.start).days]
        except KeyError:
            print("Item does not exist in count.")
        except IndexError:
            print("Date is not in count.")

    def edit(self, item, index, amt):
        """
        Edit an item.
        """
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
                date = (self.start + timedelta(i)).strftime(self.D_FORMAT)
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
