# Stalmic Distributors Inventory Count Project
# Created by Aaron Daughtry, December 12, 2016
#
# I/O functions for interactions with CSV files in a user-friendly way.

# Python 2 and 3 compatibility

from __future__ import print_function
from builtins import input

import os


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
        # Join the folder name with the filename so that we can access the
        # files while staying in the current directory.
        filelist[i] = os.path.join(folder, item)
    return filelist


def prompt_yn(string):
    """
    Prompts the user for a yes/no answer using a custom string and then returns
    True for yes or False for no.
    """
    # Keep asking for a response until a valid one is entered.
    while True:
        choice = input("\n%s [y/n]: " % string).lower()
        if choice in ('y', 'yes'):
            return True
        elif choice in ('n', 'no'):
            return False
        else:
            print("That is not a valid choice. Please try again.")


def get_csvs(folder):
    """
    Gets a list of CSV files in a directory.
    """
    csvs = []
    for file in os.listdir(folder):
        if file.lower().endswith('.csv') and not file.startswith('.'):
            csvs.append(file)
    return csvs
