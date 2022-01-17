#!/usr/bin/python

from abc import ABCMeta, abstractmethod # Used to establish an abstract base class
import os, time # Used for determining date/time of creation for files
import re # Used for matching regex to file name
from types import FunctionType # Used for creating filter functions at runtime for Complex Filters

class AbstractClassFilter(metaclass = ABCMeta):
    """Abstract Class used for filter class creation"""

    @abstractmethod
    def filter_file(self, file) -> bool:
        """Returns a boolean. True if the file passes the filter's requirements, false otherwise."""
        pass

class FileTypeFilter(AbstractClassFilter):
    """This filters files based on a file type."""
    def __init__(self, fileEnding: str):
        """instantiates the class"""
        self._fileEnding = fileEnding

    def filter_file(self, file) -> bool:
        """Returns a boolean. True if the file passes the filter's requirements, false otherwise."""
        fileType = file.name.split('.')[-1]
        return fileType == self._fileEnding

class FileCreationDateFilter(AbstractClassFilter):
    """This filters files within a date range"""
    def __init__(self, dateRange):
        """instantiates the class"""
        self._dateRange = dateRange

    def filter_file(self, file) -> bool:
        """Returns a boolean. True if the file passes the filter's requirements, false otherwise.
        This filter is currently only supports Windows"""
        UNIXTime = os.path.getctime(file.name)
        return self._dateRange[0] < UNIXTime <= self._dateRange[1]

class FileModificationDateFilter(AbstractClassFilter):
    """This filters files within a date range"""
    def __init__(self, dateRange):
        """instantiates the class"""
        self._dateRange = dateRange

    def filter_file(self, file) -> bool:
        """Returns a boolean. True if the file passes the filter's requirements, false otherwise."""
        # TODO: implement
        UNIXTime = os.path.getmtime(file.name)
        return self._dateRange[0] < UNIXTime <= self._dateRange[1]

class FileNameFilter(AbstractClassFilter):
    """This filters files whose names match a regular expression. For more
    complex filters looking to contain a regular expression, they should
    pass in .*expression.* when instantiating this filter."""

    def __init__(self, fileNameRegex: str):
        """instantiates the class"""
        self._fileNameRegex = fileNameRegex

    def filter_file(self, file) -> bool:
        """Returns a boolean. True if the file passes the filter's requirements, false otherwise."""
        regexExpression = re.compile(self._fileNameRegex)
        name = file.name.split('.')[-2].split('/')[-1] # TODO: Replace with a regular expression to get the name
        # TODO: Should this include the full path name?
        matches = regexExpression.search(name)
        # case 1: name does not contain expression
        if (not matches):
            return False
        span = matches.span()
        # cases 2/3: expression is a subset of name, name matches expression
        return (span[0] == 0 and span[1] == len(name))

class ComplexFilter(AbstractClassFilter):
    """This filter is composed of a combination of multiple base filters
    combined based on a given localical operator"""
    
    def __init__(self, logicalOperator, *args):
        # Replace args with its first entry if it is a list or tuple
        if len(args) >= 1 and (type(args[0]) == list or type(args[0]) == tuple):
            args = args[0]

        self._filters = args
            
        # Check to see if logicalOperator is a single kind
        if logicalOperator == 'and':
            self._operator = 'and'
        elif logicalOperator == 'or':
            self._operator = 'or'
        elif logicalOperator == 'not' and len(args) == 1:
            self._operator = 'not'

        else: # Logical operator is more complex
            return


    def filter_file(self, file):
        if self._operator == 'and':
            solutions = [filter.filter_file(file) for filter in self._filters]
            return not (False in solutions)
        elif self._operator == 'or':
            solutions = [filter.filter_file(file) for filter in self._filters]
            return True in solutions
        elif self._operator == 'not':
            solutions = [filter.filter_file(file) for filter in self._filters]
            return not solutions[0] # SHOULD ONLY HAVE ONE SOLUTION
        else: # ERROR
            return False

    def get_filter_file(self):
        return self._filter_function
