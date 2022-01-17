#!/usr/bin/python
import Filter as fl

class Directory():

    def __init__(*args):
        self._children = []
        self._filters = []
        for argument in args:
            if type(argument) == File:
                self._children.append(argument)
            elif type(argument) == Filter:
                self._filters.append(argument)
            else:
                print("Invalid argument passed to Directory. Argument was ignored.")
