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

import os

from count import *
from invio import *
from trucks import *
from warehouses import *


master_count = {}
for file in prompt_csvs('counts'):
    master_count[os.path.basename(file)[:-4]] = Count(file)
for file in prompt_csvs('truck invoices'):
    trk_invoices = TruckInvoices(file)
trk_loads = TruckLoads(prompt_csvs('truck loads'))
wh_invoices = WarehouseInvoices(prompt_csvs('warehouse invoices'))
wh_purchases = WarehousePurchases(prompt_csvs('warehouse purchases'))
