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

from count import Count


def prompt_csvs(type):
    """
    Promps the user for the location of CSV files of a specific type.
    """
    prompt = "Please enter the location of CSVs for %s: " % type
    folder = ''

    while os.path.isdir(folder) is False:
        folder = input(prompt)
        if os.path.isdir(folder) is False:
            print("I cannot find '%s'. Try again." % folder)

    while True:
        filelist = get_csvs(folder)
        print("\n I found %i items in %s:" % (len(filelist), folder))
        for item in filelist:
            print(item)
        if prompt_yn("Is this correct?"):
            break

    for i, item in enumerate(filelist):
        filelist[i] = os.path.join(folder, item)
    return filelist
