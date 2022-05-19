#!/usr/bin/env python3
# coding: utf-8

import json
import typer
from datetime import datetime
from timeis import timeis, yellow, green, line

from generate_html_and_json import generate_html_and_json
from helpers import get_resource_paths


app = typer.Typer()

RSC = get_resource_paths()

@app.command()
def run_generate_html_and_json(generate_roots: bool = True):
    generate_html_and_json(generate_roots)


def main():
    # Process cli with typer.
    app()

if __name__ == "__main__":
    main()
