import xmlrpc.client
from functools import partial

TeamBUAdmin = 1
TeamCoffee = 2

class Odoo:

    def __init__(self, url, db, username, password) -> None:
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        self.uid = self.common.authenticate(db, username, password, {})
        self.models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    def model(self, model):
        self.model_name = model
        return self

    def __call__(self, method, *args, **kwds):
        return self.models.execute_kw(self.db, self.uid, self.password, self.model_name, method, args, kwds)

    def __getitem__(self, indices):
        return self.model(indices)

    def __getattr__(self, name):
        return partial(self, name)

    def searchRead(self, model, conditions=[], fields={}):
        # Ensure fields is a dictionary with 'fields' key
        if 'fields' not in fields:
            fields = {'fields': fields}
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'search_read', [conditions], fields)

    def getFields(self, model, attributes={}):
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'fields_get', [], {'attributes': ['string', 'help', 'type']})

    def read(self, model, ids=[], fields={}):
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'read', ids, fields)

    def create(self, model, data):
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'create', data)

    def coffeeIssue(self, quad, subject, floor, issue):
        data = {
            'name': subject,
            'team_id': TeamCoffee,
            'description': f'quad: {quad}, floor: {floor}, Issue: {issue} '
        }
        return self.create('helpdesk.ticket', [data])

    def getHelpDeskteams(self):
        return self.models.execute_kw(self.db, self.uid, self.password, 'helpdesk.team', 'search_read', [], {})
