import os
import sys
from pathlib import Path
from typing import TypedDict
from datetime import date
from datetime import datetime
from timeis import timeis, green, red
import subprocess
import re


from dotenv import load_dotenv

import pandas as pd
from pandas.core.frame import DataFrame

load_dotenv()


class DataFrames(TypedDict):
    words_df: DataFrame
    abbrev_df: DataFrame
    help_df: DataFrame


class ResourcePaths(TypedDict):
    output_dir: Path
    output_html_dir: Path
    output_help_html_dir: Path
    output_share_dir: Path
    error_log_dir: Path
    words_path: Path
    abbrev_path: Path
    help_path: Path
    pat_words_css_path: Path
    pat_help_css_path: Path
    buttons_js_path: Path
    gd_json_path: Path


def parse_data_frames(rsc: ResourcePaths) -> DataFrames:
    """Parse csv files into pandas data frames"""

    words_df = pd.read_csv(rsc['words_path'], sep = "\t", dtype=str)
    words_df = words_df.fillna("")

    abbrev_df = pd.read_csv(rsc['abbrev_path'], sep="\t", dtype=str)
    abbrev_df.fillna("", inplace=True)

    help_df = pd.read_csv(rsc['help_path'], sep="\t", dtype=str)
    help_df.fillna("", inplace=True)

    return DataFrames(
        words_df = words_df,
        abbrev_df = abbrev_df,
        help_df = help_df
    )


def get_resource_paths() -> ResourcePaths:
    s = os.getenv('PAT_DIR')
    if s is None:
        print(f"{timeis()} {red}ERROR! PAT_DIR is not set.")
        sys.exit(2)
    else:
        pat_dir = Path(s)

    rsc = ResourcePaths(
        # Project output
        output_dir = Path("./output/"),
        output_html_dir = Path("./output/html/"),
        output_help_html_dir = Path("./output/help html/"),
        output_share_dir = Path("./share/"),
        gd_json_path = Path("./output/gd.json"),
        error_log_dir = Path("./errorlogs/"),
        # Project assets
        pat_words_css_path = Path("./assets/pat-words.css"),
        pat_help_css_path = Path("./assets/pat-help.css"),
        buttons_js_path = Path("./assets/buttons.js"),
        abbrev_path = Path("./assets/abbreviations.csv"),
        help_path = Path("./assets/help.csv"),
        # Project input
        words_path = pat_dir.joinpath("./Pātimokkha Word by Word.csv"),
    )

    # ensure write dirs exist
    for d in [rsc['output_dir'],
              rsc['output_html_dir'],
              rsc['output_share_dir'],
              rsc['error_log_dir']]:
        d.mkdir(parents=True, exist_ok=True)

    return rsc

class PATWord:
    def __init__(self, df: DataFrame, row: int):
        self.occur: str = df.loc[row, "#"]
        self.total: str = df.loc[row, "x"]
        self.pali: str = df.loc[row, "bhikkhupātimokkhapāḷi"]
        self.pos: str = df.loc[row, "pos"]
        self.grammar: str = df.loc[row, "grammar"]
        self.case: str = df.loc[row, "+case"]
        self.native: str = df.loc[row, "tamil"]
        self.meaning: str = df.loc[row, "meaning"]
        self.lit: str = df.loc[row, "lit. meaning"]
        self.root: str = df.loc[row, "root"]
        self.root_grp: str = df.loc[row, "rt gp"]
        self.root_sign: str = df.loc[row, "sign"]
        self.base: str = df.loc[row, "base"]
        self.construction: str =  df.loc[row, "construction"]
        self.comp: str = df.loc[row, "compound type"]
        self.comp_constr: str = df.loc[row, "compound construction"]
        self.rule: str = df.loc[row, "abbrev"]
        self.source: str = df.loc[row, "source"]
        self.sentence: str = df.loc[row, "sentence"]
        self.comm: str = df.loc[row, "aṭṭhakathā"]
        self.notes: str = df.loc[row, "comments"]

