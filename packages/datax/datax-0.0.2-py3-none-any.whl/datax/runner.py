import sys
import os
import click
from itertools import chain

from dxql.search import Pipeline


@click.command()
@click.option('-v', '--verbose', is_flag=True, help='Print verbose messages.')
@click.option('-i', '--interactive', is_flag=True, help='Enter into an interactive loop to query data.')
@click.option('-q', '--query', 'query_str', help='The query string.')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def main(verbose, interactive, query_str, files):
    if query_str is None and not interactive:
        sys.exit('Need query if not using interactive mode.')
    
    # if no files were provided and nothing exists in stdin
    if not files and sys.stdin.isatty():
        return
    
    open_files = []

    if files:
        if interactive:
            data_in = []
            for file_path in files:
                with open(file_path) as file:
                    data_in += file.readlines()
        else:
            open_files = [open(file_path) for file_path in files]
            data_in = chain(*open_files)
    else:
        if interactive:
            data_in = sys.stdin.readlines()
        else:
            data_in = sys.stdin
    
    if query_str:
        run_query(query_str, data_in, verbose)

    for file in open_files:
        file.close()
    
    if interactive:
        input_loop(verbose, data_in)


def run_query(query_str, data_in, verbose=False):
    results = query(query_str, data_in, verbose=verbose)
    for result in results:
        print(result)


def input_loop(verbose, data_in):
    """
    Loop and accept input for querying the data.
    """
    sys.stdin.close()

    try:
        sys.stdin = open('CON')
    except FileNotFoundError:
        sys.stdin = open('/dev/tty')

    running = True

    while running:
        try:
            print()

            s = input('> ')
            parts = s.split(' ')
            command = parts[0]

            if command == 'search':
                run_query(s, data_in, verbose)
            elif command == 'exit' or command == 'quit':
                running = False
            elif command == '':
                continue
            else:
                print(f'Unknown command: {command}')
                continue
        except KeyboardInterrupt:
            running = False

    print()
    

def query(query_str, data_in, verbose=False):
    """
    Run a query against the data and yield the results.
    :param query_str:
    :param files: list of files to query against
    :param verbose: print verbosely
    """
    if verbose:
        print(f'query: {query_str}')

    pipeline = Pipeline.create_pipeline(query_str, verbose)

    events = pipeline.execute(data_in)
    for event in events:
        yield event


def run():
    try:
        main()
    except Exception as e:
        print('FATAL ERROR')
        raise


if __name__ == '__main__':
    run()
