# -*- coding: utf-8 -*-
"""
Console script for true_path
"""
import click
from . import true_path


@click.command()
@click.argument('address')
@click.option('--verbose', '-v', is_flag=True, default=False,
              help='If set, the output is far richer')
def main(address, verbose):
    """
    A tool for checking website address' genuineness and safety.
    In order to do so, program checks the use of HTTPS and certificate
    correctness, whether the site is reachable and popular andif it's not
    marked by Google as unsafe.

    Required ADDRESS argument is a full address, like:
    https://www.example.com/eg?q=whatever
    """
    result = true_path.suite(address, verbose)
    return result


if __name__ == "__main__":
    main()
