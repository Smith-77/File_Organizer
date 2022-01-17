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

    # CHILD functions________________________________________________________________
    def add_child(self, new_child):
        if type(new_child) == Directory:
            self._children.append(new_child)
        else: # ERROR
            print("WARNING: Child was not a Directory object. Attempt to add failed")

    def get_children(self):
        return self._children

    def remove_child(self, child):
        if type(child) == Directory:
            try:
                self._children.remove(child)
                return True
            except(ValueError):
                return False
        else: # ERROR
            print("WARNING: Child was not a Directory object. Attempt to remove failed")
            return False

    def clear_children(self):
        self._children = []

    def move_child_up(self, child):
        old_index = self._children.index(child)
        if old_index == 0:
            return False
        self._children.remove(child)
        self._children.insert(old_index - 1, child)
        return True

    def move_child_down(self, child):
        try:
            old_index = self._children.index(child)
            if old_index == len(self._children) - 1:
                return False
            self._children.remove(child)
            self._children.insert(old_index + 1, child)
            return True
        except:
            return False

    # FILTER functions______________________________________________________________
    def get_filters(self):
        return self._filters
    
    def add_filter(self, new_filter):
        if filter in self._filters: # ERROR
            print("WARNING: Filter was already added. Attempt to add failed.")
        else: # WARNING: any incorrect argument won't get caught
            self._filters.append(new_filter)

    def remove_filter(self, filter):
        self._filters.remove(filter)
        return True

    def clear_filters(self):
        self._filters = []

    # This function logically combines all the file's filters with AND
    def filter_file(self, file):
        results = [filter.filter_file(file) for filter in self._filters]
        return not (False in results)

    # PATH functions_______________________________________________________________
    def set_path(self, path):
        self._path = path

    def get_path(self):
        return self._path

    # DEBUG functions______________________________________________________________
    def __str__(self):
        return self._name

    def print_children(self):
        for child in self._children:
            print(child)
