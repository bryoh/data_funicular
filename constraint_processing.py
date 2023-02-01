"""
The structure of each stderr message is
Time | Command| Severity| Message| Text file| Source unit| Data file| Tags
Where time is in the following format  YYYY-MM-DD HH:mm:SS.ms

"""

import re, fileinput
from datetime import datetime


def get_constraint(line):
    if ('CONSTRAINT' not in line) and ('Unexpected' not in line):
        return False
    constraint_pattern =re.compile('Q_[\w+.*]+|')
    constraint = constraint_pattern.findall(line)
    return ''.join(constraint)


def get_all_constraints(f_in=None):
    if f_in is None:
        f_in = 'AllConstraints.txt'  # use this data if we are extending this script
    buf = ''
    objects = []
    for line in fileinput.input():
        buf += line
        if buf.count('|') < 7:
            continue
        c = get_constraint(buf)
        if c and (c != ''):
            objects.append(ConstraintObj(buf))
        buf = ''
    return objects


class ConstraintObj:
    def __init__(self, line_str):
        line_str = str(line_str).replace('\n', '')
        items = line_str.split('|')
        self.date_str, self.line_no, self.debug_lvl, self.msg, self.text_file, self.src_uni, self.data_file, self.tag =items
        self.whole_msg = line_str
        self.constraint = get_constraint(line_str)
        self.date_obj = datetime.strptime(self.date_str, '%Y-%m-%d %H:%M:%S.%f')


if __name__ == '__main__':
    a = get_all_constraints()
    a.sort(key = lambda x: str(x.date_obj.minute))  # sort by minute
    for i in a:
        print(f'{i.date_str}, {i.constraint}, {i.whole_msg}')
