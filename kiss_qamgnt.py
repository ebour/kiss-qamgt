import argparse
import csv
import os

import pandas as pd
import pandasql as pdsql
from jinja2 import FileSystemLoader, Environment, select_autoescape
from os.path import isfile, join


def read_content(input_file):
    dict_list = []
    with open(input_file, 'rb') as file:
        reader = csv.DictReader(file)
        for line in reader:
            dict_list.append(line)
    return dict_list


def get_query_filepath(query_filename):
    if not query_filename.endswith('.sql'):
        query_filename += '.sql'
    queries_dir = globals()['QUERIES_DIR']
    return os.path.join(queries_dir, query_filename)


def query(query_filename, args=None):
    query = None
    with open(get_query_filepath(query_filename), 'r') as query_file:
        query = query_file.readline()
    if args:
        query = query % (args)

    print(query_filename + '->' + query)
    data = pdsql.PandaSQL()(query, globals()['env'])
    dict = data.to_dict('records')
    print(dict)
    return dict


def render(template_name):
    env = globals()['ENVIRONMENT']
    template = env.get_template(template_name)
    report = template.render()
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some csv file to html/pdf report files.')
    parser.add_argument('-i', type=str, help='input')
    parser.add_argument('-td', type=str, help='templates dir')
    parser.add_argument('-t', type=str, help='template')
    parser.add_argument('-qd', type=str, help='queries dir')
    parser.add_argument('-o', type=str, help='output')

    args = parser.parse_args()

    globals()['QUERIES_DIR'] = os.path.abspath(args.qd)
    globals()['TEMPLATES_DIR'] = os.path.abspath(args.td)

    env = Environment(loader=FileSystemLoader(globals()['TEMPLATES_DIR']), autoescape=select_autoescape(['html', 'xml']))
    globals()['ENVIRONMENT'] = env

    env = env.globals
    input_dir = os.path.abspath(args.i)

    files = [join(input_dir, f) for f in os.listdir(input_dir) if isfile(join(input_dir, f))]
    for file in files:
        table = os.path.basename(file.replace(input_dir, '').replace('.csv', ''))
        env[table] = pd.read_csv(file)

    report_dir = os.path.dirname(os.path.abspath(args.o))
    if os.path.exists(report_dir):
        os.makedirs(report_dir, exist_ok=True)

    env['query'] = query
    # env['render'] = render
    globals()['env'] = env

    template_name = args.t
    report = render(template_name)

    report_filepath = os.path.abspath(args.o)
    with open(report_filepath, 'w') as file:
        file.write(report)

