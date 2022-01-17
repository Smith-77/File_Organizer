#!/usr/bin/python

import Filter as fl
import Directory as dr
import Controller as ct

# Sample Filter Script
def test():
    typeFilters = []
    textFiles = fl.FileTypeFilter('txt')
    pythonFiles = fl.FileTypeFilter('py')
    sampleFile = fl.FileNameFilter('.*sample.*')

    textAndSample = fl.ComplexFilter('and', textFiles, sampleFiles)

    textAndSampleFolder = dr.Directory('text_and_sample', textAndSample)
    pythonFolder = dr.Directory('python_stuff', pythonFiles)

def main():
    controller = ct.Controller('./')
    controller.execute()

if __name__ == "__main__":
    main()
