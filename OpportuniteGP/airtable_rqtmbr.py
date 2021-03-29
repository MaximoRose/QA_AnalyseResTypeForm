# Passer dans le shell OS la commande :
#       pip3 install airtable-python-wrapper
# Tuto suivi : https://pythonhowtoprogram.com/how-to-update-the-airtable-using-python3/
import os
from pprint import pprint
from airtable import Airtable

# extraction de ma liste d'organismes stockee dans AirTable
# la colonne chaineYT contient l'url de la chaine qui correspond parfois a un user
# la colonne Secteur contient le secteur d'activite de l'organisme
# la colonne Type contient le Type de structure de l'organisme
# necessite de stocker l'info pour varier mon mode d'appel pour l'API YT

class atListe:

    def __init__(self, baseId, tableName,at_APIkey):
        self.base_id = baseId
        self.table_name = tableName
        self.at_APIkey = at_APIkey
        self.airtable = Airtable(baseId, tableName, at_APIkey)

    def get_at_AllRecords(self):
        pages = self.airtable.get_all()
        return pages

    def print_first_record(self):
        pages = self.airtable.get_iter(maxRecords=1)
        for page in pages:
            for record in page:
                pprint(record) 


