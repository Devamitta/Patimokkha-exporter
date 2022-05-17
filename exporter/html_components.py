import re

from datetime import date
from typing import TypedDict
from helpers import PATWord
from mako.template import Template

header_tmpl = Template(filename='./assets/templates/header.html')
feedback_tmpl = Template(filename='./assets/templates/feedback.html')

def render_header_tmpl(css: str, js: str) -> str:
    return str(header_tmpl.render(css=css, js=js))

def render_feedback_tmpl(w: PATWord) -> str:
    today = date.today()
    return str(feedback_tmpl.render(w=w, today=today))

class RenderResult(TypedDict):
  html: str

def render_word_meaning(w: PATWord) -> RenderResult:
    html_string = ""

    html_string += f"""<div class="content_pat"><p>"""

    html_string += f"""{w.rule}.{w.source}."""

    html_string += f""" <b>{w.sentence}</b>"""

    html_string += f"""</p></div>"""

    return RenderResult(
        html = html_string,
    )
