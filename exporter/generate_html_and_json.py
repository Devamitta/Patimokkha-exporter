import pickle
import re
from datetime import date
from datetime import datetime
import stat
import time
import pandas as pd
import os
from timeis import timeis, yellow, green, red, line

from helpers import DataFrames, PATWord, ResourcePaths, get_resource_paths, parse_data_frames
from html_components import render_header_tmpl, render_feedback_tmpl, render_word_meaning


def generate_html_and_json(generate_roots: bool = True):
    rsc = get_resource_paths()

    data = parse_data_frames(rsc)
    today = date.today()

    print(f"{timeis()} {yellow}generate html and json")
    print(f"{timeis()} {line}")
    print(f"{timeis()} {green}generating PAT html")

    error_log = open(rsc['error_log_dir'].joinpath("exporter errorlog.txt"), "w")

    html_data_list = []

    df = data['words_df']
    df_length = data['words_df'].shape[0]

    with open(rsc['pat_words_css_path'], 'r') as f:
        words_css = f.read()

    with open(rsc['buttons_js_path'], 'r') as f:
        buttons_js = f.read()

    for row in range(df_length):

        w = PATWord(df, row)

        if row % 5000 == 0 or row % df_length == 0:
            print(f"{timeis()} {row}/{df_length}\t{w.pali}")

        html_string = ""

        # html head & style

        html_string += render_header_tmpl(css=words_css, js=buttons_js)

        html_string += "<body>"

        # summary

        r = render_word_meaning(w)
        html_string += r['html']

        # buttons

        html_string += f"""<div class="button-box">"""

        if w.pali != "":
            html_string += f"""<a class="button_pat" href="javascript:void(0);" onclick="button_click(this)" data-target="summary_pat_{w.pali}">summary</a>"""

        if w.pos != "":
            html_string += f"""<a class="button_pat" href="javascript:void(0);" onclick="button_click(this)" data-target="detail_pat_{w.pali}">details</a>"""

        html_string += f"""<a class="button_pat" href="javascript:void(0);" onclick="button_click(this)" data-target="feedback_pat_{w.pali}">feedback</a>"""
        html_string += f"""</div>"""

        # summary

        html_string += f"""<div id="summary_pat_{w.pali}" class="content_pat hidden">"""
        html_string += f"""<table class = "table1_pat">"""

        if w.pali != "":
            html_string += f"""<tr valign="top"><th>Pāli</th><td>{w.pali}</td></tr>"""

        if w.pos != "":
            html_string += f"""<tr><th>Grammar</th><td>{w.pos}"""

        if w.grammar != "":
            html_string += f""", {w.grammar}"""

        if w.case != "":
            html_string += f""" ({w.case})"""

        html_string += f"""</td></tr>"""

        html_string += f"""<tr valign="top"><th>Meaning</th><td><b>{w.meaning}</b></td></tr>"""

        html_string += f"""</table>"""
        html_string += f"""<p><a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdG6zKDtlwibtrX-cbKVn4WmIs8miH4VnuJvb7f94plCDKJyA/viewform?usp=pp_url&entry.438735500={w.pali}&entry.1433863141=Pātimokkha analysis {today}" target="_blank">Report a mistake.</a></p>"""
        html_string += f"""</div>"""

        # details

        html_string += f"""<div id="details_pat_{w.pali}" class="content_pat hidden">"""
        html_string += f"""<table class = "table1_pat">"""

        if w.lit != "":
            html_string += f"""</td></tr>"""
            html_string += f"""<tr valign="top"><th>Literally</th><td>{w.lit}</td></tr>"""

        if w.root != "":
            html_string += f"""<tr valign="top"><th>Root</th><td>{w.root} {root_grp} {root_sign}</td></tr>"""

        if w.base != "":
            html_string += f"""<tr valign="top"><th>Base</th><td>{w.base}</td></tr>"""

        if w.construction != "":
            html_string += f"""<tr valign="top"><th>Construction</th><td>{w.construction}</td></tr>"""
            construction_text = re.sub("<br/>", ", ", w.construction)

        if w.comp != "":
            html_string += f"""<tr valign="top"><th>Compound</th><td>{w.comp} ({w.comp_constr})</td></tr>"""

        if w.comm != "":
            html_string += f"""<tr valign="top"><th>Commentary</th><td>{w.comm}</td></tr>"""

        # if w.notes != "":
        #     html_string += f"""<tr valign="top"><th>Notes</th><td>{w.notes}</td></tr>"""

        html_string += f"""</table>"""
        html_string += f"""<p><a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdG6zKDtlwibtrX-cbKVn4WmIs8miH4VnuJvb7f94plCDKJyA/viewform?usp=pp_url&entry.438735500={w.pali}&entry.1433863141=Pātimokkha analysis {today}" target="_blank">Report a mistake.</a></p>"""
        html_string += f"""</div>"""


        html_string += render_feedback_tmpl(w)

        html_string += f"""</body></html>"""


        # data compiling

        html_data_list += [[f"{w.pali}", f"""{html_string}"""]]

        if row % 100 == 0:
            p = rsc['output_html_dir'].joinpath(f"{w.pali} (sample).html")
            with open(p, "w", encoding="utf-8") as f:
                f.write(html_string)

        
# convert ṃ to ṁ

    # text_data_full = re.sub("ṃ", "ṁ", text_data_full)
    # text_data_concise = re.sub("ṃ", "ṁ", text_data_concise)


def generate_roots_html_and_json(data: DataFrames, rsc: ResourcePaths, html_data_list):

    # pali_data_df = pd.DataFrame(html_data_list)
    # pali_data_df.columns = ["word", "definition_html", "definition_plain", "synonyms"]


    # generate abbreviations html

    print(f"{timeis()} {green}generating abbreviations html")

    abbrev_data_list = []

    with open(rsc['pat_help_css_path'], 'r') as f:
        abbrev_css = f.read()

    abbrev_df = data['abbrev_df']
    abbrev_df_length = len(abbrev_df)

    for row in range(abbrev_df_length):
        
        html_string = ""

        abbrev = abbrev_df.iloc[row,0]
        meaning = abbrev_df.iloc[row,1]
        
        css = f"{abbrev_css}"
        html_string += render_header_tmpl(css=css, js="")

        html_string += "<body>"

        # summary

        html_string += f"""<div class="help_pat"><p>abbreviation. <b>{abbrev}</b>. {meaning}</p></div>"""
        
        p = rsc['output_help_html_dir'].joinpath(f"{abbrev}.html")

        with open(p, 'w') as f:
            f.write(html_string)
        
        # compile root data into list
        synonyms = [abbrev,meaning]
        abbrev_data_list += [[f"{abbrev}", f"""{html_string}""", "", synonyms]]

# generate help html

    print(f"{timeis()} {green}generating help html")

    help_data_list = []

    with open(rsc['pat_help_css_path'], 'r') as f:
        help_css = f.read()

    help_df = data['help_df']
    help_df_length = len(help_df)

    for row in range(help_df_length):
        
        html_string = ""

        help_title = help_df.iloc[row,0]
        meaning = help_df.iloc[row,1]
        
        css = f"{help_css}"
        html_string += render_header_tmpl(css=css, js="")

        html_string += "<body>"

        # summary

        html_string += f"""<div class="help_pat"><p>help. <b>{help_title}</b>. {meaning}</p></div>"""
        
        p = rsc['output_help_html_dir'].joinpath(f"{help_title}.html")

        with open(p, 'w') as f:
            f.write(html_string)
        
        # compile root data into list
        synonyms = [help_title]
        help_data_list += [[f"{help_title}", f"""{html_string}""", "", synonyms]]


        
    # roots > dataframe > json

    print(f"{timeis()} {green}generating json")

    abbrev_data_df = pd.DataFrame(abbrev_data_list)
    abbrev_data_df.columns = ["word", "definition_html", "definition_plain", "synonyms"]

    help_data_df = pd.DataFrame(help_data_list)
    help_data_df.columns = ["word", "definition_html", "definition_plain", "synonyms"]

    pali_data_df = pd.concat([pali_data_df, abbrev_data_df, help_data_df])

    print(f"{timeis()} {green}saving html to json")

    pali_data_df.to_json(rsc['gd_json_path'], force_ascii=False, orient="records", indent=6)

    print(f"{timeis()} {line}")


def delete_unused_html_files():
    print(f"{timeis()} {green}deleting unused html files")
    now = datetime.now()
    date = now.strftime("%d")
    for root, dirs, files in os.walk("output/html/", topdown=True):
        for file in files:
            stats = os.stat(f"output/html/{file}")
            mod_time = time.ctime (stats [stat.ST_CTIME])
            mod_time_date = re.sub("(.[^ ]+) (.[^ ]+) (.[^ ]+).+", r"\3", mod_time)
            if date != int(mod_time_date):
                try:
                    os.remove(f"output/html/{file}")
                    print(f"{timeis()} {file}")
                except:
                    print(f"{timeis()} {red}{file} not found")
    
    print(f"{timeis()} {green}deleting unused roots html files")
    for root, dirs, files in os.walk("output/root html/", topdown=True):
        for file in files:
            stats = os.stat(f"output/root html/{file}")
            mod_time = time.ctime (stats [stat.ST_CTIME])
            mod_time_date = re.sub("(.[^ ]+) (.[^ ]+) (.[^ ]+).+", r"\3", mod_time)
            if date != int(mod_time_date):
                try:
                    os.remove(f"output/root html/{file}")
                    print(f"{timeis()} {file}")
                except:
                    print(f"{timeis()} {red}{file} not found")