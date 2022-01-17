#!/usr/bin/python

import os
import DirectoryTree as dt
import Directory as dr
import Filter as fl

class Controller:

    def __init__(self, source_directory_path):
        self._source_directory_path = source_directory_path

        # Collect source files
        self._source_files = []
        for files in os.listdir(source_directory_path):
            possible_file = os.path.join(source_directory_path, files)
            if os.path.isfile(possible_file):
                self._source_files.append(possible_file)

        # establish DirectoryTree
        root_directory = self._create_directory_structure()
        self._directory_tree = dt.DirectoryTree(root_directory, self._source_files)

        print(self._source_files)
        # print(self._directory_tree.get_root_directory().get_children())

    def _create_directory_structure(self):
        typeFilters = []
        textFiles = fl.FileTypeFilter('txt')
        pythonFiles = fl.FileTypeFilter('py')
        sampleFiles = fl.FileNameFilter('.*sample.*')

        textAndSample = fl.ComplexFilter('and', textFiles, sampleFiles)

        textAndSampleFolder = dr.Directory('text_and_sample', textAndSample)
        pythonFolder = dr.Directory('python_stuff', pythonFiles)

        root_directory = dr.Directory('root', [textAndSampleFolder, pythonFolder])
        t = open("sample.py")
        print(textAndSample.filter_file(t))
        print(textAndSampleFolder.filter_file(t))
        return root_directory

    def execute(self):
        work_left = True
        while work_left:
            work_left = self._directory_tree.visit_next_directory()
