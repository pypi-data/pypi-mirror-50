import click
from flask import current_app
from flask.cli import with_appcontext
from invenio_access import ActionSystemRoles, any_user
from invenio_accounts.models import Role, User
from invenio_db import db

#
# Taxonomies commands
#
from flask_taxonomies.models import Taxonomy
from flask_taxonomies.permissions import (
    taxonomy_create_all,
    taxonomy_delete_all,
    taxonomy_read_all,
    taxonomy_term_create_all,
    taxonomy_term_delete_all,
    taxonomy_term_move_all,
    taxonomy_term_read_all,
    taxonomy_term_update_all,
    taxonomy_update_all,
)


@click.group()
def taxonomies():
    """Taxonomies commands."""


#
# Taxonomies subcommands
#
@taxonomies.command('all-read')
@with_appcontext
def all_read():
    """Set permissions for everyone to read all taxonomies and taxonomy terms."""
    db.session.add(ActionSystemRoles.allow(taxonomy_read_all, role=any_user))
    db.session.add(ActionSystemRoles.allow(taxonomy_term_read_all, role=any_user))
    db.session.commit()


@taxonomies.command('all-modify')
@with_appcontext
def all_modify():
    """Set permissions for everyone to read all taxonomies and taxonomy terms."""
    db.session.add(ActionSystemRoles.allow(taxonomy_create_all, role=any_user))
    db.session.add(ActionSystemRoles.allow(taxonomy_update_all, role=any_user))
    db.session.add(ActionSystemRoles.allow(taxonomy_delete_all, role=any_user))
    db.session.add(ActionSystemRoles.allow(taxonomy_term_create_all, role=any_user))
    db.session.add(ActionSystemRoles.allow(taxonomy_term_update_all, role=any_user))
    db.session.add(ActionSystemRoles.allow(taxonomy_term_delete_all, role=any_user))
    db.session.add(ActionSystemRoles.allow(taxonomy_term_move_all, role=any_user))
    db.session.commit()


@taxonomies.command('import')
@click.argument('taxonomy_file')
@click.option('--int', 'int_conversions', multiple=True)
@click.option('--drop/--no-drop', default=False)
@with_appcontext
def import_taxonomy(taxonomy_file, int_conversions, drop):
    from .import_export import import_taxonomy
    import_taxonomy(taxonomy_file, int_conversions, drop)


@taxonomies.command('list')
@with_appcontext
def list_taxonomies():
    for t in Taxonomy.taxonomies():
        print(t.code)


@taxonomies.command('delete')
@click.argument('code')
@with_appcontext
def delete_taxonomy(code):
    t = Taxonomy.get(code)
    db.session.delete(t)
    db.session.commit()
