# -*- coding: utf-8 -*-
import os
import click
import subprocess
import sqlite3

from ..main import odoo

from ..utils import manage_error
from crontab import CronTab
import requests
import json

URL = 'https://eynes.com.ar/eeodoo/translations/'
HEADERS = {'Content-Type': 'application/json'}


def echo_success():
    click.secho('Success!', fg='green', blink=True, bold=True)


@manage_error
def connect_db():
    click.echo('--> Connecting to local DB ', nl=False)
    home = os.path.expanduser("~")
    local_db = sqlite3.connect(home + '/eeodoo_translations.db')
    cr = local_db.cursor()
    create_table = """
        CREATE TABLE IF NOT EXISTS eeodoo_translations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT UNIQUE NOT NULL,
            translation TEXT NOT NULL,
            sync BOOLEAN DEFAULT(0)
        );
    """
    cr.execute(create_table)
    echo_success()
    return local_db, cr


# @manage_error
def odoo_connection(action, values=[]):
    assert action in ['retrieve', 'update'], 'action is not valid'
    assert isinstance(values, list), 'values must be a list'
    data = {"params":{
        'action': action,
        # 'values': [{'source':'a','dest':'b'}]}
        'values': values}
    }
    data_json = json.dumps(data)
    r = requests.post(url=URL, data=data_json, headers=HEADERS)
    res = r.json()
    return res

# @manage_error
def sync(local_db, cr):
    click.echo('--> Fetching from odoo:')
    i18n_in_server = odoo_connection('retrieve')
    server_translations = i18n_in_server.get('result')
    if server_translations:
        warning_label = click.style('WARNING!', bold=False, fg='yellow')
        done_label = click.style('DONE!', bold=False, fg='green')
        for entry in server_translations:
            try:
                cr.execute("INSERT INTO eeodoo_translations (origin, translation, sync) VALUES ('%s', '%s', 1)" % (entry['source'], entry['dest']))
            except Exception as e:
                click.echo(warning_label + ' Translation for %s already in local storage' % entry['source'])
                local_db.rollback()
            else:
                click.echo(done_label + ' Translation for %s updated in local storage to %s' % (entry['source'], entry['dest']))
                local_db.commit()
    cr.execute("SELECT origin as source, translation as dest FROM eeodoo_translations WHERE sync=0")
    todo_list = [{'source': i[0], 'dest': i[1]} for i in cr.fetchall()]
    if todo_list:
        odoo_connection('update', todo_list)
        cr.execute("UPDATE eeodoo_translations SET sync=1 WHERE sync=0")
        local_db.commit()

def install_cron():
    click.echo('You are going to create a cron that runs sync_translations automatically.')
    if not click.confirm('Do you want to continue?'):
        return
    qty_hour = click.prompt('Cron interval (Hour/s)', default=4, type=int)
    cron = CronTab(user=True)
    job = cron.new(command='eeodoo sync_translations &> /tmp/eeodoo_sync.log')
    job.hour.every(qty_hour)
    cron.write()


@odoo.command()
@click.option('-i', '--install',
              help="Install cron", default=False, is_flag=True)
def sync_translations(install):
    """
    Export po file, translate it automaticaly and copy to i18n path.
    """
    if install:
        install_cron()
    else:
        # Connect to local DB
        local_db, cr = connect_db()

        # Sync DBs
        sync(local_db, cr)

    click.echo('Goodbye!')
