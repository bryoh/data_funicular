'''
Given a list of csv files, plots each csv file on a web page
you need to have dygraph libraries in a folder nameed dygraph

dygraph-----|
            |_______dygraph.css
            |_______dygraph.min.js
dygrap_data |
            |_______file1.csv
            |_______file2.csv
'''

import os
def head():
    return """
    <head>
    <script type='text/javascript'src="dygraph/dygraph.min.js"></script><link rel='stylesheet' src='dygraph/dygraph.css'/>
    </head>
    """


def body(divs, scripts):
    # scripts need to the bottom of the page in order to speed up rendering
    return """
    <body>{} 
    <script>
    {}
    </script>
    </body>""".format(divs, scripts)


def create_div(element_id):
    # given an element id create div
    return '''
    <h2>{0}</h2>
    <div id={0} style="width: 50% !important; margin-top: 50px; margin-bottom: 50px;"></div>'''.format(element_id)


def format_javascript(csv, element_id):
    # given a csv and an element id create javascript
    obj_name = element_id.replace('/','')
    # return ''' {0}jObject = new Dygraph(document.getElementById('{1}'), "{2}", { {rollPeriod: 7, showRoller: true}});'''.format(obj_name, element_id,csv)
    return ''' %sObject = new Dygraph(document.getElementById('%s'), "%s",  {rollPeriod: 7, showRoller: true});
    ''' %(obj_name, element_id, csv)


def create_graph(csv, value):
    # given a csv return two items a div and the javascript part
    div_id = "{1}{0}".format(str(value), str(csv).replace('.csv', ''))
    html = create_div(div_id)
    javascript_part = format_javascript(csv, div_id)
    return html, javascript_part


def create_graphs(csv_s):
    # given a list of csvs create a list of tuples [(div),(javascript)]
    if isinstance(csv_s, str):
        return create_graph(csv_s, 1)

    div_parts = javascript_parts = ''
    for value, csv_file in enumerate(csv_s):
        div_part, javascript_part = create_graph(csv_file, value)
        div_parts += div_part
        javascript_parts += javascript_part
    return div_parts, javascript_parts


def construct_page(csv_s, output_file_name):
    # give a csv(or list of csvs) and output filename
    # this will create a html file in the current working directory
    header_str = head()
    divs, scripts = create_graphs(csv_s)
    body_str = body(divs, scripts)
    whole_thing = '<html>' + header_str + body_str + '</html>'
    with open(output_file_name, 'w+') as html_file:
        html_file.write(whole_thing)


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
    print(dir(args))
    for file in os.listdir(args.usr_folder):
        print(paths)
        if str(file).endswith('csv'):
            paths.append(file)
    construct_page(paths, os.path.join(args.usr_folder,'index.html'))