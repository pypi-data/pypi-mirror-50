import collections

import requests

from . import auth

class BinderAPI:
    DEFAULT_HOST = 'https://api.gmbinder.com'

    # Document returns more fields but only these are needed
    Document = collections.namedtuple('Document', 'title key markdown_key')

    def __init__(self, username, password, *, host=DEFAULT_HOST):
        self.host = host
        self.auth = auth.BinderAuth(username, password, host=self.host)


    def get_doc(self, doc):
        r = requests.get(
                f'{self.host}/documents/{doc.key}',
                auth=self.auth,
        )
        return r.json()['markdown']['value']

    def get_docs(self, *, archived=False):
        # Required to set getArchived, else api quietly defaults to true
        # bool in request needs to be lower case, api violates json spec
        # can't pass in params raw as it's serialized 'True' or 'False'
        params = { 'getArchived': str(archived).lower() }
        r = requests.get(
                f'{self.host}/documents',
                params=params,
                auth=self.auth,
        )

        def extract_doc(d):
             return self.Document(d['title'], d['key'], d['markdownKey'])
        return [extract_doc(d) for d in r.json()]

    def get_all_docs(self):
        return self.get_docs() + self.get_docs(archived=True)


    def archive_doc(self, doc):
        self.archive_key(doc.key)

    def archive_key(self, key):
        requests.delete(
                f'{self.host}/documents/{key}/archive',
                auth=self.auth
        )


    def delete_doc(self, doc):
        self.delete_key(doc.key)

    def delete_key(self, key):
        requests.delete(
                f'{self.host}/documents/{key}',
                auth=self.auth
        )


    def new_doc(self, title):
        params = { 'shareSource': 'true', 'title': title }
        r = requests.post(
                f'{self.host}/documents',
                json=params,
                auth=self.auth
        )

        def extract_doc(d):
            f = d['file']
            return self.Document(f['title'], d['key'], f['markdownKey'])

        return extract_doc(r.json())

    def update_doc(self, doc, content, *, variables=None):
        milliseconds = int(round(time.time() * 1000))
        params = {
                'data': {
                        'markdownKey': doc.markdown_key,
                },
                'key': doc.key,
                'markdown': {
                        'updated_at': milliseconds,
                        'value': content,
                },
        }

        if variables is not None:
            def make_variables(d):
                return [{'varName': k, 'varValue': v} for k, v in d.items()]

            params['data']['variables'] = make_variables(variables)
        
        r = requests.post(
                f'{self.host}/documents',
                json=params,
                auth=self.auth
        )