import requests
import re
import argparse
import csv
import progressbar

subcommand = 'csv-export'

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def export_csv(filename, secret_key, domain, original_url_column, path_column, title_column, created_at_column, cloaking, delimiter, **kwargs):
    with open(filename) as f:
        csv_reader = csv.reader(f, delimiter=delimiter)
        lines = [line for line in csv_reader]
        links_count = len(lines)
        link_chunks = chunks(lines, 1000)
        pb = progressbar.ProgressBar(widgets=[
            progressbar.Percentage(),
            ' ',
            progressbar.Counter(),
            progressbar.Bar(),
            progressbar.AdaptiveETA()
        ], max_value=links_count)
        for idx, chunk in enumerate(link_chunks):
            r = requests.post('https://api.short.cm/links/bulk', headers={
                'Authorization': secret_key,
            }, json=dict(
                domain=domain,
                allowDuplicates=kwargs['allow_duplicates'],
                links=[
                    dict(
                        originalURL=chunk_item[original_url_column],
                        cloaking=int(cloaking),
                        path=re.sub('https?://[^/]+/', '', chunk_item[path_column]) if path_column is not None else None,
                        title=chunk_item[title_column] if title_column is not None else None,
                        createdAt=arrow.get(chunk_item[created_at_column]).format() if created_at_column is not None else None,
                    ) for chunk_item in chunk
                ]
            ))
            r.raise_for_status()
            pb.update(idx * 1000)


def add_parser(subparsers):
    import_parser = subparsers.add_parser('csv-export', help='Short.cm to CSV')
    import_parser.add_argument('--filename', dest='filename', help='Filename to import', required=True)
    import_parser.add_argument('--domain', dest='domain', help='Short domain', required=True)
    import_parser.add_argument('--cloaking', default=0, type=int, dest='cloaking', help='Cloaking enabled, default - disabled')
    import_parser.add_argument('--delimiter', default=',', dest='delimiter', help='CSV delimiter, by default – ,')
    import_parser.add_argument('--allow-duplicates', default=0, type=int, dest='allow_duplicates', help='Allow original URL dupilcates')
    import_parser.add_argument('--path-column', dest='path_column', help='Column number (starting from 0) for path', type=int)
    import_parser.add_argument('--original-url-column', dest='original_url_column', help='Column number (starting from 0) for original URL', required=True, type=int)
    import_parser.add_argument('--title-column', dest='title_column', help='Column number (starting from 0) for link title', type=int)
    import_parser.add_argument('--created-at-column', dest='created_at_column', help='Column number (starting from 0) for link creation date', type=int)
    return import_parser


def run_command(args):
    import_csv(**vars(args))

