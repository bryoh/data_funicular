"""
From a folder of csv files (for example processing/ ) this script produces a folder called output_data/ with processed csv and an index.html.
By processed I mean that the dates are formatted accordingly.

+--- processing
|   +--- accDataInstant.csv
|   +--- ACCmessages.csv
|   +--- AGDLMessages.csv
|   +--- CCAMSAverage.csv
|   +--- CCAMSCumulative.csv
|   +--- CCAMSMessages.csv
|   +--- CCDSRAverage.csv
|   +--- CCDSRCumulative.csv
|   +--- CCDSRMessages.csv
|   +--- ifplAverage.csv
|   +--- ifplCumulative.csv
|   +--- IFPLmessages.csv
|   +--- mtcdDataInstant.csv
+--- simpleserver3.py
+--- perf_tools.py
+--- dygraph.py
+--- fmt_csvs_dates.py
"""
from shutil import rmtree

from itertools import chain
import fmt_csvs_dates, dygraph
import os, datetime, re, webbrowser


def create_folder(folder_name):
    """ creates a folder named dygraph_data if it does not already exist """
    if os.path.exists(folder_name):
        rmtree(folder_name)
    return os.makedirs(folder_name)


def str_to_date_obj(str, fmt=None):
    if fmt is None:
        fmt='%Y-%m-%d'
    return datetime.datetime.strptime(str, fmt)


def try_regex(pattern, string):
    ret =None
    pat = pattern.replace('\\d', '\d')  # not necessary but ...
    my_string = "".join(str(string))
    try:
        ret = re.findall(pat, my_string )[0]
    except Exception as e:
        pass
        #print('EXCEPTION: "{}" found on {}'.format(e, string))
    return ret


def day_has_passed(past, present):
    hr_val = past.hour > present.hour
    day_diff = (present - past).total_seconds() >= 86400
    return hr_val or day_diff


def add_date(list_of_str, time_fmt='%H:%M:%S', d=None, m=None, yr=None, time_regex=None):
    list_obj = []
    now = datetime.datetime.now()
    d = now.day if d is None else d
    m = now.month if m is None else m
    yr = now.year if yr is None else yr
    time_regex = r'(\d{2}:\d{2})' if time_regex is None else time_regex
    #time_regex = r'\d{2}:\d{2}:\d{2}' if time_regex is None else time_regex

    current_date = datetime.datetime(yr, m, d)
    past = current_date  # Both equal since there is no previous
    for i in list(list_of_str):
        regs = try_regex(time_regex, "".join(chain(*i)))
        if regs is None:
            #print('Skipping since not time object is found in line: {!s}'.format(str(i)))
            continue

        i_obj = datetime.datetime.strptime(regs, time_fmt).time()
        current_date = current_date.combine(current_date, i_obj)
        sentence = [str(current_date)]
        sentence.extend(i[1:])
        list_obj.append(sentence)
        if day_has_passed(past, current_date):
            current_date += datetime.timedelta(days=1)
        past = current_date
    return list_obj


def csvs_to_dygraph(input_folder, date_str,destination_folder='output_data'):
    create_folder(destination_folder)
    paths = []
    for filename in os.listdir(input_folder):
        if '.csv' not in filename:
            continue
        paths.append(filename)
        #open, read csv converting adding date. and return a list
        formated_csv_data = fmt_csvs_dates.read_csv(os.path.join(input_folder, filename))
        fmt_csvs_dates.write_csv(formated_csv_data, filename, destination_folder)

    dygraph.construct_page(paths, os.path.join(destination_folder, 'index.html'))


if __name__ == '__main__':
    csvs_to_dygraph('processing', '20171016')
    # import http.server
    # import socketserver
    #
    # PORT = 8000
    #
    # Handler = http.server.SimpleHTTPRequestHandler
    #
    # with socketserver.TCPServer(("", PORT), Handler) as httpd:
    #     print("serving at port", PORT)
    #     httpd.serve_forever()
    #
    # url = simpleserver3.run()
    # port = url.split(':')[1]
    # webbrowser.open_new_tab(url)  # 2 to open in a new tab if possible