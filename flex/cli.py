import click
from flex.core import load


@click.command()
@click.option('-s',
              help='Source; a url to a schema or a file path to a schema')
def main(s):
    """For a given command line supplied argument, negotiate
     the content, parse the schema and then 
    return any issues to stdout or if no schema issues, 
    return success exit code."""
    if s is None:
        print(
            """You need to supply a file to a schema or 
            a url to a schema, for the validator to work.""")
        return 0
    try:
        load(s)
        print('Validation passed')
        return 1
    except ValueError, e:
        print(e.message)
        return 0


if __name__ == '__main__':
    main()
