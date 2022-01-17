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
    def __init__(self, *args):
        """instantiates the class"""
        print("Creating new FileTypeFilter...")
        self._fileEndings = []
        self._negativeFileEndings = []
        self.add_file_endings(args)

    def filter_file(self, file) -> bool:
        """Returns a boolean. True if the file type is one of the specified types or if the
        file type is NOT one of the negative specified file types, assuming no positive file
        types are given. False otherwise."""
        fileType = file.name.split('.')[-1]
        if len(self._fileEndings) > 0:
            return (fileType in self._fileEndings)
        else:
            return not fileType in self._negativeFileEndings

    def _add_file_endings(self, args):
        for arg in args:
            if type(arg) == list or type(arg) == tuple:
                    self._add_file_endings(arg)
            elif isinstance(arg, str) and len(arg) >= 2:
                if arg[0] == '.':
                    self._fileEndings.append(arg[1:])
                elif arg[0] == '!' and arg[1] == '.':
                    self._negativeFileEndings.append(arg[2:])
                else:
                    print("\tWARNING: Inappropriate file ending, %s, ignored. File endings must begin with '.' or '!.'" % (arg))
            else:
                print("\tWARNING: Inappropriate file ending ignored. File endings must be strings.")

    def add_file_endings(self, *args):
        self._add_file_endings(args)
        # Warn user if some endings are being ignored
        if len(self._fileEndings) != 0 and len(self._negativeFileEndings) != 0:
            print("\tWARNING: All negative file types were ignored because positive file types were given.")

    def get_file_endings(self):
        return [self._fileEndings, self._negativeFileEndings]

class FileCreationDateFilter(AbstractClassFilter):
    """This filters files within a date range"""
    def __init__(self, dateRange):
        """instantiates the class"""
        print("Creating new FileCreationDateFilter...")
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
        print("Creating new FileModificationDateFilter...")
        self._dateRange = dateRange

    def filter_file(self, file) -> bool:
        """Returns a boolean. True if the file passes the filter's requirements, false otherwise."""
        # TODO: implement
        UNIXTime = os.path.getmtime(file.name)
        return self._dateRange[0] < UNIXTime <= self._dateRange[1]

class FileNameMatchesFilter(AbstractClassFilter):
    """This filters files whose names match a regular expression. For more
    complex filters looking to contain a regular expression, they should use
    the FileNameContainsFilter or pass in .*expression.* when instantiating this filter."""

    def __init__(self, fileNameRegex: str):
        """instantiates the class"""
        print("Creating new FileNameMatchesFilter...")
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

class FileNameContainsFilter(AbstractClassFilter):
    """This filters files whose names contains a set of regular expression."""

    def __init__(self, *args):
        self._regular_expressions = []
        self.add_expressions(args)

    def add_expressions(self, *args):
        self._add_expressions(args)

    def _add_expressions(self, args):
        for arg in args:
            if type(arg) == list or type(arg) == tuple:
                    self._add_expressions(arg)
            elif isinstance(arg, str) and len(arg) >= 0:
                self._regular_expressions.append(arg)
            else:
                print("\tWARNING: Inappropriate regular expression ignored. Regular expressions must be non-empty strings.")

    def filter_file(self, file) -> bool:
        """Returns a boolean. True if the file contains all of the regular expressions"""
        for regular_expression in self._regular_expressions:
            regexExpression = re.compile(regular_expression)
            name = file.name.split('.')[-2].split('/')[-1] # TODO: Replace with a regular expression to get the name
            # TODO: Should this include the full path name?
            matches = regexExpression.search(name)
            # case 1: name does not contain expression
            if (not matches):
                return False
        
        # All regular expressions contained within file name - file passes
        return True

class LogicFilter(AbstractClassFilter):
    """This filter is composed of a combination of multiple base filters
    combined based on a given localical operator"""
    
    def __init__(self, logicalOperator, *args):
        print("Creating new LogicFilter...")
        # Replace args with its first entry if it is a list or tuple
        if len(args) >= 1 and (type(args[0]) == list or type(args[0]) == tuple):
            args = args[0]

        # Cleanup logicalOperator
        logicalOperator = logicalOperator.lower() 

        # Set filters property which holds all filters being combined in logic filter
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
