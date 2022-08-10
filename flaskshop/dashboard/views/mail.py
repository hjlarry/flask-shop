from flask import render_template, redirect, url_for, request
from sqlalchemy import or_
from flask_babel import lazy_gettext

def mails():
    page = request.args.get("page", type=int, default=1)
    search_word = request.args.get("keyword")