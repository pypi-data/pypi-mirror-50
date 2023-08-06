#!/usr/bin/env python3
import argparse
import json
import os
import sys

import requests

from .api import BinderAPI
from .printing import column_print

def cli_print_doc(api, args):
    from browsermobproxy import Server

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    

    app_state = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }

    chrome_prefs = {
        "printing.print_preview_sticky_settings.appState": json.dumps(app_state),
    }


    server = Server("path/to/browsermob-proxy")
    server.start()
    server.add_header('Authorization','Bearer ' + token)
    proxy = server.create_proxy()


    token = api.auth.request_token()

    chrome_options = ChromeOptions()
    profile.set_proxy(proxy.selenium_proxy())
    chrome_options.add_argument('--kiosk-printing')
    #chrome_options.add_argument("--headless")
    chrome_options.set_proxy(proxy.selenium_proxy())
    chrome_options.add_experimental_option('prefs', chrome_prefs)

    driver = webdriver.Chrome(
        executable_path='/Users/swetrist/Downloads/chromedriver',
        options=chrome_options,
        )

    driver.get(f'https://www.gmbinder.com/documents/print/{doc.key}')
    print_button = driver.find_element_by_class_name('btn-primary') 
    print_button.click()


    server.stop()
    driver.quit()


def cli_list_docs(api, args):
    docs = api.get_docs(archived=args.archived)
    column_print(docs, headers=api.Document._fields)


def cli_add_doc(api, args):
    doc = api.new_doc(args.doc_name or os.path.basename(args.file))
    with open(args.file) as f:
        api.update_doc(doc, f.read())

    print(f'Uploaded "{doc.title}" id:"{doc.key}"')


def selector(args, doc):
    if args.key is not None:
        return doc.key == args.key
    elif args.title is not None:
        return doc.title == args.title
    else:
        return doc.title == os.path.basename(args.file)


def cli_push_doc(api, args):
    for d in api.get_all_docs():
        if selector(args, d):

            with open(args.file) as f:
               api.update_doc(d, f.read())

            print(f'Pushed "{d.title}" id:"{d.key}"')
            break
            
    else:
        print(f'Could not push "{d}" (not found)', file=sys.stderr)
            

def cli_pull_doc(api, args):
    for d in api.get_all_docs():
        if selector(args, d):
            with open(args.file, 'w') as f:
                f.write(api.get_doc(d))

            print(f'Pulled "{d.title}" id:"{d.key}"')
            break
    else:
        print(f'Could not pull "{d}" (not found)', file=sys.stderr)


def cli_archive_docs(api, args):
    docs = api.get_docs(archived=args.archived)
    pprint.pprint(docs.json())


def cli_delete_docs(api, args):
    if args.pattern:
        for d in api.get_all_docs():
            if args.pattern in d.title:
                print(f'Deleteing "{d.title}" id:"{d.key}" (pattern match)')
                api.delete_doc(d)

    docs = api.get_all_docs()
    titles = {d.title: d.key for d in docs}
    keys = {d.key: d.title for d in docs}

    if args.documents:
        for d in args.documents:
            if d in keys:
                api.delete_key(d)
                print(f'Deleteing "{keys[d]}" id:"{d}" (key match)')
            elif d in titles:
                api.delete_key(titles[d])
                print(f'Deleteing "{d}" id:"{titles[d]}" (title match)')
            else:
                print(f'Could not delete "{d}" (not found)', file=sys.stderr)


def add_document_select_group(parser):
    select_group = parser.add_argument_group('document selection',
            'Specifies how to find document (default: --title)')
    mutex_group = select_group.add_mutually_exclusive_group()
    mutex_group.add_argument('--title',
            help='Title of document (default: filename)')
    mutex_group.add_argument('--key', help='Key of document')


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-dir', default='.',
            help=('Directory to look for tool configuration files in '
                 '(default: ".")'))
    parser.add_argument('--credentials', default='credentials',
            help=('JSON credentials for authorization '
                  '(default: "config-dir/credentials")'))
    parser_subs = parser.add_subparsers(dest='command', required=True)

    docs_parser = parser_subs.add_parser('docs', help='Manipulate documents')
    docs_parser_subs = docs_parser.add_subparsers(dest='subcommand',
            required=True)

    def add_doc_list_parser(subparsers):
        parser = subparsers.add_parser('list', help='List documents')
        parser.set_defaults(func=cli_list_docs)
        parser.add_argument('--archived', action='store_true',
                help='List archived projects rather than active')

    def add_doc_add_parser(subparsers):
        parser = subparsers.add_parser('add', help='Upload a new document')
        parser.set_defaults(func=cli_add_doc)
        parser.add_argument('file', help='File to upload')
        parser.add_argument('--title',
                help='Title to create in gmbinder (default: filename)')

    def add_doc_push_parser(subparsers):
        parser = subparsers.add_parser('push',
                help='Push an update to a document')
        parser.set_defaults(func=cli_push_doc)
        parser.add_argument('file', help='File to push from')
        add_document_select_group(parser)

    def add_doc_pull_parser(subparsers):
        parser = subparsers.add_parser('pull', 
                help='Pull an update from a document')
        parser.set_defaults(func=cli_pull_doc)
        parser.add_argument('file', help='File to pull to')
        add_document_select_group(parser)

    def add_doc_delete_parser(subparsers):
        parser = subparsers.add_parser('delete', help='Delete a document')
        parser.set_defaults(func=cli_delete_docs)
        parser.add_argument('--pattern',
                help='Delete all documents with title matching pattern')
        parser.add_argument('--documents', nargs=argparse.REMAINDER,
                help='List of documents by id or title to delete')


    add_doc_list_parser(docs_parser_subs)
    add_doc_add_parser(docs_parser_subs)
    add_doc_push_parser(docs_parser_subs)
    add_doc_pull_parser(docs_parser_subs)
    add_doc_delete_parser(docs_parser_subs)

    args = parser.parse_args()

    with open(os.path.join(args.config_dir, args.credentials)) as f:
        config = json.load(f)

    api = BinderAPI(config['username'], config['password'])
    args.func(api, args)


if __name__ == '__main__':
    cli()