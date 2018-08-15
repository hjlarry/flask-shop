# -*- coding: utf-8 -*-
"""Click commands."""
from subprocess import call
import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound
from pathlib import Path
from itertools import chain

from flaskshop.random_data import (
    create_users,
    create_menus,
    create_addresses,
    create_shipping_methods,
    create_products_by_schema,
    create_page,
    create_collections_by_schema,
    create_admin,
    create_orders,
    create_product_sales,
    create_vouchers
)

HERE = Path(__file__).resolve()
PROJECT_ROOT = HERE.parent
TEST_PATH = PROJECT_ROOT / "tests"


@click.command()
def test():
    """Run the tests."""
    import pytest

    rv = pytest.main([TEST_PATH, "--verbose"])
    exit(rv)


@click.command()
@click.option(
    "-f",
    "--fix-imports",
    default=False,
    is_flag=True,
    help="Fix imports using isort, before linting",
)
def lint(fix_imports):
    """Lint and check code style with flake8 and isort."""
    skip = ["node_modules", "requirements"]
    root_files = Path(PROJECT_ROOT).glob("*.py")
    root_directories = (file for file in Path(PROJECT_ROOT).iterdir() if not file.name.startswith("."))

    files_and_directories = [
        arg.name for arg in chain(root_files, root_directories) if arg.name not in skip
    ]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo("{}: {}".format(description, " ".join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool("Fixing import order", "isort", "-rc")
    execute_tool("Checking code style", "flake8")


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.

    Borrowed from Flask-Script, converted to use Click.
    """
    for file in chain(Path(PROJECT_ROOT).glob("**/*.pyc"), Path(PROJECT_ROOT).glob("**/*.pyo")):
        click.echo("Removing {}".format(file))
        file.unlink()


@click.command()
@click.option("--url", default=None, help="Url to test (ex. /static/image.png)")
@click.option(
    "--order", default="rule", help="Property on Rule to order by (default: rule)"
)
@with_appcontext
def urls(url, order):
    """Display all of the url matching routes for the project.

    Borrowed from Flask-Script, converted to use Click.
    """
    rows = []
    column_length = 0
    column_headers = ("Rule", "Endpoint", "Arguments")

    if url:
        try:
            rule, arguments = current_app.url_map.bind("localhost").match(
                url, return_rule=True
            )
            rows.append((rule.rule, rule.endpoint, arguments))
            column_length = 3
        except (NotFound, MethodNotAllowed) as e:
            rows.append(("<{}>".format(e), None, None))
            column_length = 1
    else:
        rules = sorted(
            current_app.url_map.iter_rules(), key=lambda rule: getattr(rule, order)
        )
        for rule in rules:
            rows.append((rule.rule, rule.endpoint, None))
        column_length = 2

    str_template = ""
    table_width = 0

    if column_length >= 1:
        max_rule_length = max(len(r[0]) for r in rows)
        max_rule_length = max_rule_length if max_rule_length > 4 else 4
        str_template += "{:" + str(max_rule_length) + "}"
        table_width += max_rule_length

    if column_length >= 2:
        max_endpoint_length = max(len(str(r[1])) for r in rows)
        # max_endpoint_length = max(rows, key=len)
        max_endpoint_length = max_endpoint_length if max_endpoint_length > 8 else 8
        str_template += "  {:" + str(max_endpoint_length) + "}"
        table_width += 2 + max_endpoint_length

    if column_length >= 3:
        max_arguments_length = max(len(str(r[2])) for r in rows)
        max_arguments_length = max_arguments_length if max_arguments_length > 9 else 9
        str_template += "  {:" + str(max_arguments_length) + "}"
        table_width += 2 + max_arguments_length

    click.echo(str_template.format(*column_headers[:column_length]))
    click.echo("-" * table_width)

    for row in rows:
        click.echo(str_template.format(*row[:column_length]))


@click.command()
@click.option("--type", default="default", help="which type to seed")
@with_appcontext
def seed(type):
    if type == "default":
        place_holder = Path("placeholders")
        create_products_by_schema(
            placeholder_dir=place_holder, how_many=10, create_images=True
        )
        create_generator = chain(create_collections_by_schema(place_holder), create_users(), create_addresses(),
                                 create_page(), create_menus(), create_shipping_methods(), create_orders(),
                                 create_product_sales(), create_vouchers(), create_admin())
        for msg in create_generator:
            click.echo(msg)
    else:
        create_dict = {
            "user": create_users,
            "menu": create_menus,
            "address": create_addresses,
            "ship": create_shipping_methods,
            "order": create_orders,
            "sale": create_product_sales,
            "voucher": create_vouchers
        }
        fn = create_dict[type]
        for msg in fn():
            click.echo(msg)
