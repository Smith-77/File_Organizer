#!/usr/bin/python

import os
import DirectoryTree as dt
import Directory as dr
import Filter as fl

class Controller:

    def __init__(self, dest_directory_path):
        self._dest_directory_path = dest_directory_path

        # establish DirectoryTree
        root_directory = self._create_directory_structure()
        self._directory_tree = dt.DirectoryTree(self._dest_directory_path, root_directory)

    def _create_directory_structure(self):
        print("\nDESIGNING DIRECTORY STRUCTURE:\n*************************************")
        # Establish basic filters
        nonJavaFilter = fl.FileTypeFilter('!.java')
        sampleFiles = fl.FileNameContainsFilter('am')

        # Create Complex Filters
        notSample = fl.LogicFilter('not', sampleFiles)
        nonDirectoryPython = fl.LogicFilter('not', fl.FileNameMatchesFilter('.*Directory.*'))

        # Create directories
        sampleFiles = dr.Directory('sampleFiles', sampleFiles)

        nonJavaFiles = dr.Directory('nonJavaFiles', nonJavaFilter)
        nonDirectory = dr.Directory('nonDirectory', nonDirectoryPython)
        nonJavaFiles.add_child(nonDirectory)

        nonJavaFiles2 = dr.Directory('nonJavaFiles2', nonJavaFilter)

        # Construct and return root directory
        root_directory = dr.Directory('root', [sampleFiles, nonJavaFiles])
        root_directory.add_child(nonJavaFiles2)
        root_directory.move_child_up(nonJavaFiles2)
        root_directory.move_child_up(nonJavaFiles2)
        print(nonJavaFiles.get_filters())
        nonJavaFiles.remove_filter(nonJavaFilter)
        return root_directory

    def execute(self, create_new=False, create_all=True):
        print("\nEXECUTING:\n*************************************")
        if (len(self._directory_tree.get_source_files()) <= 0):
            print("\tWARNING: No source files found. Load source files to populate the directory structure.")
        work_left = True
        while work_left:
            work_left = self._directory_tree.visit_next_directory(replace=create_new, create_full_structure=create_all)

    def delete_source_files(self, exceptions=[]):
        source_files = self._directory_tree.get_source_files()
        print("Deleting source files...")
        if len(source_files) == 0:
            print("\tWARNING: No source files to delete.")
            return
        # print("Deleting %r source files from %s..." % (len(source_files), self._source_directory_path))
        [self._delete_file(file) for file in source_files if not (file in exceptions)]
            
    def _delete_file(self, file_path):
        try:
            os.remove(file_path)
        except:
            print("\tWARNING: Attempt to delete %s failed." % (file_path))

    def collect_source_files(self, source_directory_path, recursive=False):
        print("\nLOADING SOURCE FILES:\n*************************************")
        files = self._get_source_files(source_directory_path, source_files=[], recursive=recursive)
        self._directory_tree.add_source_files(files)

    def _get_source_files(self, directory_path, source_files, recursive=False):
        print("Loading source files from %s ..." % (directory_path))
        for object in os.listdir(directory_path):
            item = os.path.join(directory_path, object)
            if os.path.isfile(item):
                source_files.append(item)
            elif recursive and os.path.isdir(item):
                self._get_source_files(item, source_files, recursive=True)
        return source_files
