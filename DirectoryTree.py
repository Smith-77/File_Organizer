#!/usr/bin/python

import os

from queue import Queue

import shutil

class DirectoryTree:

    def __init__(self, root_path, root_directory):
        # Root should have no filters itself
        self._root_directory = root_directory
        self._current_directory = root_directory
        self._source_files = []

        # Create queue and add root directory
        self._visited_directories = []
        self._directory_queue = Queue(maxsize = 0)
        self._root_directory.set_path(root_path + '\\' + self._root_directory.get_name())
        self._directory_queue.put_nowait(self._root_directory)

    """ replace:True - existing directories with same names will be destroyed and replaced
                False - existing directories will be filled with any new source files
        create_full_structure:True - all directories specified in structure will be created
                              False - all internal directories will be created and 'leaf'
                                      directories that have at least one file in it.
        When adding one or a few files to an existing file structure, it's suggested that
        replace = False and create_full_structure = False
    """
    def visit_next_directory(self, replace=False, create_full_structure=True):
        """ Visits next directory in the queue, adds its children to the queue, and creates the
        directory with files. Returns true if there's more directories to visit """
        # If queue is empty, it is done
        if self._directory_queue.empty():
            print("No more directories to visit - All Done!")
            return False

        # Visit new directory
        self._current_directory = self._directory_queue.get_nowait()
        self._mark_directory_as_visited(self._current_directory)

        # Create current directory if called for/necessary and fill it up
        new_dir_path = self._current_directory.get_path()
        print("Creating new directory: %s ..." % (new_dir_path))
        try:
            os.mkdir(new_dir_path)
        except:
            if (replace):
                shutil.rmtree(new_dir_path)
                print("\tReplacing direcotry %s ..." % (new_dir_path))
                try:
                    os.mkdir(new_dir_path)
                except:
                    print("\t\tWARNING: Failure to replace %s." % (new_dir_path))
            else:
                print("\tWARNING: Failure to create %s." % (new_dir_path))

        # Fill the directory with files
        print("Filling directory %s with files ..." % (new_dir_path))
        files_added = False
        try:
            files_added = self._fill_directory(self._current_directory)
        except:
            print("\tWARNING: Failure to fill directory %s with files. More detailed error messages can be added later" % (new_dir_path))

        # Add children to back of the queue and set their paths if they haven't been visited and
        # There's files left or the full directory structure should be created
        # TODO: won't update the full structure. If I add a file in a folder to which no new source files are added, then the file I added doesn't get filtered further...
        if (files_added or create_full_structure == True):
            for child in self._current_directory.get_children():
                if not self._directory_was_visited(child):
                    child.set_path(self._current_directory.get_path() + '\\' + child.get_name())
                    self._directory_queue.put_nowait(child)
        elif (len(os.listdir(new_dir_path)) <= 0): # Remove directory if it's empty and create_full_structure
            os.rmdir(new_dir_path)


        return True

    def _fill_directory(self, directory):
        if directory == self._root_directory:
            for file in self._source_files:
                file_name = file.split('\\')[-1]
                dest_path = directory.get_path() + '\\' + file_name
                shutil.copyfile(file, dest_path)
            return True
        else:
            parent_path = directory.get_path()[:len(directory.get_path()) - len(directory.get_name()) - 1]
            files = self._get_file_names(parent_path)
            file_added = False
            for file in files:
                f = open(file, 'r')
                if directory.filter_file(f):
                    f.close()
                    file_name = file.split('\\')[-1]
                    dest_path = directory.get_path() + '\\' + file_name
                    # TODO: add try/except
                    shutil.move(file, dest_path)
                    file_added = True
            return file_added

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
        pass

    def get_root_directory(self):
        return self._root_directory

    def add_source_files(self, files):
        for file in files:
            self._source_files.append(file)

    def get_source_files(self):
        return self._source_files
        
