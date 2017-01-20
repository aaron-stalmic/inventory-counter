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
from transfers import *

wh_names = {
           'WH#1 Townsend': 'wh1',
           'WH#2 Lakeland': 'wh2',
           'Drop Ship': 'dropship'
}

route_key = {
            '- Deliveries':     'wh1',
            '- Drop Ship':      'dropship',
            '- Shipping - GA':  'wh1',
            '*DLR':             'wh1',
            'CTO':              'wh1',
            'FL1 - GA Central': 'wh1',
            'FL1 - GaN':        'wh1',
            'FL1 - GA-S/FL-N':  'wh1',
            'FL1 - JAX':        'wh1',
            'FL1 - SC':         'wh1',
            'FL1 - SC+D&G':     'wh1',
            'FL2 - FlaE':       'wh2',
            'FL2 - FlaK':       'wh2',
            'FL2 - FlaM':       'wh2',
            'FL2 - FlaO':       'wh2',
            'FL2 - FlaW':       'wh2',
            'RS1 - AM':         'wh1',
            'RS1 - AR':         'wh1',
            'RS1 - CR':         'wh1',
            'RS1 - DR':         'wh1',
            'RS1 - NF':         'wh1',
            'RS1 - SC':         'wh1',
            'RS1 - SR':         'wh1',
            'RS2 - FC':         'wh2',
            'RS2 - FE':         'wh2',
            'RS2 - FM':         'wh2',
            'RS2 - FW':         'wh2',
            'TECH1 - GK':       'wh1',
            'TECH2 - DA':       'wh2',
            'TECH3 - DC':       'wh2',
            'TLDR1 - CO':       'wh1',
            'TLDR2 - JJ':       'wh2',
            'zz_TEST2':         'wh2',
            'zzTEST - ATL':     'wh2'
}


master_count = {}
for file in prompt_csvs('counts'):
    master_count[os.path.basename(file)[:-4]] = Count(file)
trk_invoices = TruckInvoices(prompt_csvs('truck invoices')[0])
transfers = Transfers(prompt_csvs('transfers')[0], wh_names)
trk_loads = TruckLoads(prompt_csvs('truck loads'))
wh_invoices = WarehouseInvoices(prompt_csvs('warehouse invoices'))
wh_purchases = WarehousePurchases(prompt_csvs('warehouse purchases'))
