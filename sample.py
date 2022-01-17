#!/usr/bin/python

import Filter as fl
import Directory as dr
import Controller as ct

# TODO: who/how is the directory structure constructed
# Deleting files from source after or as it goes as an option
# Order of filters added is important, option to copy files belonging to multiple folders or better options to specify order of filters?

def main():
    controller = ct.Controller('.\\sandbox')
    controller.collect_source_files('./sandbox', recursive=True)
    controller.execute(create_new=False, create_all=True)
    controller.delete_source_files()


if __name__ == "__main__":
    main()
