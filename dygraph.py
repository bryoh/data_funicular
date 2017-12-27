'''
Given a list of csv files, plots each csv file on a web page
you need to have dygraph libraries in a folder nameed dygraph

run
python -m SimpleHTTPServer

to serve on local host
'''

import os, shutil, time
import fmt_csvs_dates
import perf_tools

def head():
    return """
    <!DOCTYPE html>
    <head>
    <meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7; IE=EmulateIE9">
    <script type='text/javascript'src="dygraph/dygraph.min.js"></script><link rel='stylesheet' src='dygraph/dygraph.css'/>
    </head>
    """


def body(divs, scripts):
    # scripts need to the bottom of the page in order to speed up rendering
    return """
    <body>
        <div>
            {}
        </div> 
        <script>{}</script>
    </body>""".format(divs, scripts)


def create_div(element_id):
    # given an element id create div
    return '''
    <h2>{0}</h2>
    <div id={0} style="width: 90% !important; margin-top: 20px; margin-bottom: 20px;"></div>'''.format(element_id)


def format_javascript(csv, element_id, folder):
    # given a csv and an element id create javascript
    obj_name = element_id.replace('/','')
    absolute_csv_location = os.path.join(folder, csv)
    common_path= os.path.commonprefix([os.getcwd(), absolute_csv_location]) # "{}\{}".format(folder, csv)
    csv_location = absolute_csv_location.replace(common_path, '')
    print(csv_location)
    return ''' {0}Object = new Dygraph(document.getElementById('{1}'), "{2}",  {{titleHeight: 32 }});'''.format(obj_name, element_id, csv_location.replace('\\', '/'))


def create_graph(csv, value, folder=None):
    # given a csv return two items a div and the javascript part
    div_id = "{1}{0}".format(str(value), str(csv).replace('.csv', ''))
    html = create_div(div_id)
    javascript_part = format_javascript(csv, div_id, folder)
    return html, javascript_part


def create_graphs(csv_s, folder=None):
    # given a list of csvs create a list of tuples [(div),(javascript)]
    if isinstance(csv_s, str):
        return create_graph(csv_s, 1)

    div_parts = javascript_parts = ''
    for value, csv_file in enumerate(csv_s):
        div_part, javascript_part = create_graph(csv_file, value, folder)
        div_parts += div_part
        javascript_parts += javascript_part
    return div_parts, javascript_parts


def construct_page(csv_s, output_file_name, folder=None):
    # give a csv(or list of csvs) and output filename
    # this will create a html file in the current working directory
    header_str = head()
    divs, scripts = create_graphs(csv_s, folder)
    print(scripts)
    body_str = body(divs, scripts)
    whole_thing = '<html>' + header_str + body_str + '</html>'
    with open(output_file_name, 'w+') as html_file:

        html_file.write(whole_thing)


def copy_file(src, dest):
    try:
        return shutil.copy(src, dest)
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Copy Error: %s' % e.strerror)
    print('Source: {!s} , Destination: {!s}'.format(src, dest))


def is_valid_file(parser, arg):
    """ Check if arg is a valid file that already exists on the file system. """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def get_parser():
    """Get parser object for script """
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--usr_folder", dest="usr_folder", type=lambda x: is_valid_file(parser, x),
                        help="Insert the path to the folder with csv files", metavar="file")
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    paths = []

    usr_folder = args.usr_folder
    processing_folder = 'processing/'
    destination_folder = 'output_data/'
    #shutil.rmtree(processing_folder)
    #shutil.rmtree(destination_folder)
    perf_tools.create_folder(processing_folder)
    perf_tools.create_folder(destination_folder)

    for file_name in os.listdir(usr_folder):
        if str(file_name).endswith('.csv'):
            copy_file(os.path.join(usr_folder,file_name), processing_folder)

    for file_name in os.listdir(processing_folder):
        if str(file_name).endswith('csv'):
            paths.append(file_name)
            new_csv_list = fmt_csvs_dates.read_csv(os.path.join(processing_folder, file_name))

            fmt_csvs_dates.write_csv(new_csv_list, os.path.join(destination_folder, file_name))

    construct_page(paths, 'index.html', destination_folder)
