import os
import settings
from airtable import Airtable

api_key = os.environ.get('AIRTABLE_API_KEY')
table_name = os.environ.get('AIRTABLE_TABLE_NAME')
base_id = os.environ.get('AIRTABLE_BASE_ID')
staging_mentors_table = Airtable(base_id, table_name, api_key=api_key)

production_base_id = os.environ.get('AIRTABLE_PRODUCTION_BASE_ID')
production_mentors_table = Airtable(production_base_id, table_name, api_key=api_key)

print(staging_mentors_table, production_mentors_table)