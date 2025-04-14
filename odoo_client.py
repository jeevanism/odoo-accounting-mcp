import os
import re
import socket
import urllib.parse
import xmlrpc.client


class OdooClient:
    def __init__(self, url, db, username, password):
        if not re.match(r"^https?://", url):
            url = f"http://{url}"
        url = url.rstrip("/")

        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None

        self._common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        self._models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        self._connect()

    def _connect(self):
        self.uid = self._common.authenticate(self.db, self.username, self.password, {})
        if not self.uid:
            raise ValueError("Authentication failed")

    def search_read(self, model, domain=[], fields=None, limit=10):
        return self._models.execute_kw(
            self.db,
            self.uid,
            self.password,
            model,
            "search_read",
            [domain],
            {"fields": fields, "limit": limit}
        )


def get_odoo_client():
    return OdooClient(
        url=os.environ["ODOO_URL"],
        db=os.environ["ODOO_DB"],
        username=os.environ["ODOO_USERNAME"],
        password=os.environ["ODOO_PASSWORD"]
    )
