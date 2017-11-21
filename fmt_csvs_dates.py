#/usr/bin/python
# -*- coding: utf-8 -*-
"""Given the start date of the test and a folder with the output of franscripts, this program creates a folder with a
list of csv where the timestamp field is formated with yyyy-mm-dd HH:MM:ss.sss
"""
from shutil import rmtree
import os, csv, re, datetime
import perf_tools


def get_parser():
    """Get parser object for script """
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '-date', dest='start_date', action='store', help='Execution date in the following format "yyyy-mm-dd" ')
    parser.add_argument('-f', '-files', dest='folder', action='store', help='The path of the generated files')
    return parser


def read_csv(file, begin_date=None, time_fmt='%H:%M:%S', date_fmt='%Y%M%d', time_regex=r'\d{2}:\d{2}:\d{2}'):
    """ reads and formats the timestamp column of each csv then returns a list of rows"""
    ret = []
    if begin_date and date_fmt:
        var_date = perf_tools.str_to_date_obj(begin_date, date_fmt)
    else:
        var_date = datetime.datetime.now()
    yr, m, d = var_date.year, var_date.month, var_date.day

    with open(file, 'r') as rfile:
        reader = csv.reader(rfile)
        ret.append(next(reader, None))
        ret.extend(perf_tools.add_date(reader, time_fmt, d, m, yr, time_regex))

    return ret


def write_csv(list_obj, save_name, folder_name=''):
    destination_path = os.path.join(folder_name, save_name)
    with open(destination_path, 'w+') as raw_file:
        new_data = csv.writer(raw_file, dialect='excel', delimiter=',', escapechar=' ', lineterminator='\n',
                              quoting=csv.QUOTE_NONE)
        for i in list_obj:
            new_data.writerow(i)
