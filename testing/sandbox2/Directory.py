#!/usr/bin/python
import Filter as fl
import os # For creating directories
import shutil # For moving files

class Directory:

    def __init__(self, name: str, *args):
        self._name = name
        self._children = []
        self._filters = []
        self._add_filter_or_child(args)
        self._path = ''
        # os.mkdir(name)

    def _add_filter_or_child(self, things_to_add):
        for thing in things_to_add:
            if type(thing) == list or type(thing) == tuple:
                self._add_filter_or_child(thing)
            elif type(thing) == Directory:
                self.add_child(thing)
            else: # WARNING: any incorrect argument won't be checked to be a filter!!!
                self.add_filter(thing)

    def get_name(self) -> str:
        return self._name

    def add_child(self, new_child):
        if type(new_child) == Directory:
            self._children.append(new_child)
        else: # ERROR
            print("Child was not a Directory object. Attempt to add failed")

    """ def add_child(self, new_child):
        self.print_children()

        print("===========================")
        if not self._new_child_is_valid(new_child): # ERROR
            print("Child was already found. Attempt to %s add failed." % (new_child.get_name()))
        elif type(new_child) == Directory:
            print(new_child)
            self._children.append(new_child)
            self.print_children()
            print("&&&&&&&&&&&&&&&&&&&&&&&")
        else: # ERROR
            print("Child was not a Directory object. Attempt to add failed")
        self.print_children()
        print("**************************") """

    def get_children(self):
        return self._children

    def clear_children(self):
        self._children = [] 

    """ def _new_child_is_valid(self, new_child) -> bool:
        new_group = new_child.get_children()
        new_group.append(new_child)
        current_group = self._children
        current_group.append(self)
        intersect = [directory for directory in new_group if directory in current_group]
        return len(intersect) == 0 """

    def add_filter(self, new_filter):
        if filter in self._filters: # ERROR
            print("Filter was already added. Attempt to add failed.")
        else: # WARNING: any incorrect argument won't get caught
            self._filters.append(new_filter)

    def clear_filters(self):
        self._filters = []

    """ def add_files(self, *args):
        for argument in args:
            if type(argument) == list or type(argument) == tuple:
                self.add_files(argument)
            elif self.filter_file(argument):
                sourcePath = os.path.abspath(argument.name)
                targetPath = self._name + '/' + argument.name.split('/')[-1]
                shutil.copy(sourcePath, targetPath) """

    # This function logically combines all the file's filters with AND
    def filter_file(self, file):
        results = [filter.filter_file(file) for filter in self._filters]
        return not (False in results)

    def set_path(self, path):
        self._path = path

    def get_path(self):
        return self._path

    def __str__(self):
        return self._name

    def print_children(self):
        for child in self._children:
            print(child)
