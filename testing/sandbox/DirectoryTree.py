#!/usr/bin/python

import os

from queue import Queue

import shutil

class DirectoryTree:

    def __init__(self, root_directory, source_files):
        # Root should have no filters itself
        self._root_directory = root_directory
        self._current_directory = root_directory
        self._source_files = source_files

        # Create queue and add root directory
        self._visited_directories = []
        self._directory_queue = Queue(maxsize = 0)
        self._root_directory.set_path('.\\' + self._root_directory.get_name())
        self._directory_queue.put_nowait(self._root_directory)

    def visit_next_directory(self):
        """ Visits next directory in the queue, adds its children to the queue, and creates the
        directory with files. Returns true if there's more directories to visit """
        # If queue is empty, it is done
        if self._directory_queue.empty():
            return False

        # Visit new directory
        self._current_directory = self._directory_queue.get_nowait()
        self._mark_directory_as_visited(self._current_directory)

        # Add children to back of the queue if they haven't been visited and set their paths
        for child in self._current_directory.get_children():
            if not self._directory_was_visited(child):
                child.set_path(self._current_directory.get_path() + '\\' + child.get_name())
                self._directory_queue.put_nowait(child)

        # Create current directory and fill it up
        os.mkdir(self._current_directory.get_path())
        self._fill_directory(self._current_directory)

        return True

    def _fill_directory(self, directory):
        if directory == self._root_directory:
            for file in self._source_files:
                file_name = file.split('\\')[-1]
                dest_path = directory.get_path() + '\\' + file_name
                shutil.copyfile(file, dest_path)
        else:
            parent_path = directory.get_path()[:len(directory.get_path()) - len(directory.get_name()) - 1]
            files = self._get_file_names(parent_path)
            for file in files:
                f = open(file, 'r')
                if directory.filter_file(f):
                    file_name = file.split('\\')[-1]
                    dest_path = directory.get_path() + '\\' + file_name
                    shutil.move(file, dest_path)

    def _get_file_names(self, path):
        file_names = []
        for files in os.listdir(path):
            possible_file = os.path.join(path, files)
            if os.path.isfile(possible_file):
                file_names.append(possible_file)
        return file_names

    def _mark_directory_as_visited(self, directory):
        self._visited_directories.append(directory)

    def _directory_was_visited(self, directory):
        return directory in self._visited_directories

    def fill_current_directory(self, files):
        passs

    def get_root_directory(self):
        return self._root_directory
        
