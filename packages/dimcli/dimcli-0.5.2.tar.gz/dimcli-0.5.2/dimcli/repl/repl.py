#!/usr/bin/env python
"""
Autocompletion example.

Press [Tab] to complete the current word.
- The first Tab press fills in the common part of all completions
    and shows all the completions. (In the menu)
- Any following tab press cycles through all the possible completions.
"""
from __future__ import unicode_literals

from prompt_toolkit.completion import Completion, Completer
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.formatted_text import HTML

# from prompt_toolkit import prompt   #using session instead
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

import click
import json
import sys
import os
import time
import requests

from ..core.api import Dsl, USER_HISTORY_FILE, USER_JSON_OUTPUTS_DIR
from ..core.dsl_grammar import *
from ..core.utils import *

from .autocompletion import *
from .history import *
from .key_bindings import *
from .lexer import *




HELP_MESSAGE =  """DIMCLI COMMANDS HELP
====================
Default: enter a DSL query and click return to send it to the Dimensions API.
Special commands start with '.'
Tip: autocomplete works better when there are spaces between operators (eg `search where id = "xxx"`)
----
>>> help: show this help message
----
>>> <tab>:  autocomplete. 
----
>>> .docs: print out documentation for DSL data objects.  
>>> .export_as_json: save results from last query as JSON file.  
>>> .export_as_csv: save results from last query as CSV file.  
>>> .export_as_html: save results from last query as HTML file. 
>>> .show [optional: N]: print N results from last query, trying to build URLs for objects. Default N=10.
>>> .show_json_compact: print results of last query as single-line JSON. 
>>> .show_json_full: print results of last query as formatted JSON.
----
>>> <Ctrl-o>: search docs online. 
>>> <Ctrl-c>: abort query.
>>> <Ctrl-d>: exit console.
----
>>> quit: exit console
----"""

WELCOME_MESSAGE = "Welcome! Type help for more info."
# WELCOME_MESSAGE = "Welcome! Type help for more info. Ready to query endpoint: %s"



#
#
# DIMENSIONS QUERY AND DATA HANDLING
#
#


class DslResultsBuffer(object):
    current_json = ""
    current_query = ""

    def save(self, json_data, query):
        self.current_json = json_data
        self.current_query = query

    def retrieve(self):
        return (self.current_json, self.current_query)



class CommandsManager(object):

    def __init__(self, dslclient, databuffer):
        self.dsl = dslclient
        self.bf = databuffer

    def handle(self, text):
        "process text and delegate"
        if text.replace("\n", "").strip().startswith(".show"):
            self.show(text.replace("\n", "").strip())

        elif text.replace("\n", "").strip().startswith(".export"):
            self.export(text.replace("\n", "").strip())

        elif text.replace("\n", "").strip().startswith(".docs"):
            self.docs_full(text.replace("\n", "").strip())

        else:
            return self.query(text)

    def query(self, text):
        """main procedure after user query dsl"""
        # lazy complete
        text = line_add_lazy_return(text)
        text = line_add_lazy_describe(text)
        click.secho("You said: %s" % text, fg="black", dim=True)
        # RUN QUERY
        res = self.dsl.query(text)
        # #
        if "errors" in res.data.keys():
            if "query" in res.data["errors"]:
                print(res.data["errors"]["query"]["header"])
                for key in res.data["errors"]["query"]["details"]:
                    print(key)
            else:
                print(res.data["errors"])
        elif text.strip().startswith("search"):
            print_json_stats(res, text)
            if self.bf: self.bf.save(res.data, text)
            if True:
                click.secho("---", dim=True)
                preview_results(res.data, maxitems=5)
            return res  # 2019-03-31

        else:
            # describe queries and other functions: just show the data
            if self.bf: self.bf.save(res.data, text)
            click.secho("---", dim=True)
            print_json_full(res.data)


    def docs_full(self, text):
        """
        print out docs infos from 'describe' API
        """
        text = text.replace(".docs", "").split()
        if len(text) > 0:
            if text[0] in G.entities():
                res = self.dsl.query(f"describe entity {text[0]}")
            else:
                res = self.dsl.query(f"describe source {text[0]}")
            if "errors" in res.data.keys():
                print(res.data["errors"])
            # show all fields 
            click.secho("=====\nFIELDS")
            for x in sorted(res.json['fields']):
                d = res.json['fields'][x].get('description') or  ""
                typ = res.json['fields'][x].get('type', "")
                ise = res.json['fields'][x].get('is_entity', "")
                isfa = res.json['fields'][x].get('is_facet', "")
                isfi = res.json['fields'][x].get('is_filter', "")
                if isfa:
                    infos = f"[type={typ}, filter={isfi}, facet={isfa}]"
                else:
                    infos = f"[type={typ}, filter={isfi}]"
                click.echo(click.style(x, bold=True) + " " + click.style(infos, dim=True) + \
                    " " + click.style(d))
            if 'metrics' in res.json:
                click.secho("=====\nMETRICS")
                for x in res.json['metrics']:
                    d = res.json['metrics'][x]['description'] or "no description"
                    click.echo(click.style(x, bold=True) + " " + click.style(d, dim=True))
            if 'fieldsets' in res.json:
                click.secho("=====\nFIELDSETS")
                f = res.json['fieldsets']
                if f:
                    click.secho(", ".join([x for x in f]), bold=True)
            if 'search_fields' in res.json:
                click.secho("=====\nSEARCH FIELDS")
                f = res.json['search_fields']
                if f:
                    click.secho(", ".join([x for x in f]), bold=True)

        else:
            print("Please specify a source or entity.")


    def export(self, text):
        """
        save results of a query to a file
        """
        if self.bf: 
            jsondata, query = self.bf.retrieve()
        else:
            jsondata, query = None, None
        if not jsondata:
            print("Nothing to export - please run a search first.")
            return
        # cases
        if text == ".export_as_html":
            export_json_html(jsondata, query, USER_JSON_OUTPUTS_DIR)

        elif text == ".export_as_csv":
            export_json_csv(jsondata, query, USER_JSON_OUTPUTS_DIR)

        elif text == ".export_as_json":
            export_json_json(jsondata, query, USER_JSON_OUTPUTS_DIR)

    def show(self, text):
        """
        show results of a query
        """
        DEFAULT_NO_RECORDS = 10
        # text = text.replace(".show", "").strip()
        text = text.strip()

        if self.bf: 
            jsondata, query = self.bf.retrieve()
        else:
            jsondata, query = None, None
        if not jsondata:
            print("Nothing to show - please run a search first.")
            return
        # cases
        if text == ".show_json_compact":
            print_json_compact(jsondata)
        elif text == ".show_json_full":
            print_json_full(jsondata)
        else:
            # must be a simple ".show" + X command
            try:
                no = text.replace(".show", "").strip()
                slice_no = int(no)
            except ValueError:
                slice_no = DEFAULT_NO_RECORDS
            preview_results(jsondata, maxitems=slice_no)




#
#
# MAIN CLI
#
#


def run(instance="live"):
    """
    run the repl
    """

    try:
        CLIENT = Dsl(instance=instance, show_results=False)
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)

    # dynamically retrieve dsl version 
    click.secho(WELCOME_MESSAGE)
    try:
        _info = CLIENT.query("describe version")['release']
    except:
        _info = "not available"
    click.secho(f"Using endpoint: {CLIENT._url} - DSL version: {_info}", dim=True)

    # history
    session = PromptSession(history=SelectiveFileHistory(USER_HISTORY_FILE))

    databuffer = DslResultsBuffer()

    # REPL loop
    while True:
        try:
            text = session.prompt(
                "\n> ",
                default="",  # you can pass a default text to begin with
                completer=CleverCompleter(),
                complete_style=CompleteStyle.MULTI_COLUMN,
                # validator=BasicValidator(),
                # validate_while_typing=False,
                multiline=False,
                complete_while_typing=True,
                lexer=BasicLexer(),
                key_bindings=bindings,
            )
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.
        except Exception as e:
            print(e)
            sys.exit(0)  
        else:
            if text.strip() == "":
                continue
            elif text == "quit":
                break
            elif text == "help":
                click.secho(HELP_MESSAGE, dim=True)
                continue
            try:
                cm = CommandsManager(CLIENT,databuffer)
                cm.handle(text)
            except Exception as e:
                print(e)
                continue
    print("GoodBye!")


if __name__ == "__main__":
    run()
