import os
import settings
from airtable import Airtable

table_name = os.environ.get('AIRTABLE_TABLE_NAME')
base_id = os.environ.get('AIRTABLE_BASE_ID')
staging_mentors_table = Airtable(base_id, table_name)

production_base_id = os.environ.get('AIRTABLE_PRODUCTION_BASE_ID')
production_mentors_table = Airtable(production_base_id, table_name)

# print(staging_mentors_table, production_mentors_table)

# 1. get all records from production mentors table


def get_all_users_from_production_mentors_table(base, table):
    ''' Gets all the user records from the production_mentors_table'''

    production_mentors_table = Airtable(base, table)
    all_users = production_mentors_table.get_all()

    # print(all_users)
    return all_users


get_all_users_from_production_mentors_table(
    production_base_id, table_name)

# 2. insert those records to staging mentors table


def insert_all_users_to_staging_mentors_table(base, table):
    staging_mentors_table = Airtable(base, table)
    records = {
        "records": [
            {
                "fields": {
                    "Slack Name": "testmentor1",
                    "Full Name": "Testing Testerson",
                    "Skillsets": [
                        "Web (Backend Development)",
                        "Java"
                    ],
                    "What time zone are you in?": "Central",
                    "Services": [
                        "recwcy31c6wNWAUHi"
                    ],
                    "Mentor Request": [
                        "reca4PhD9FUqVR73b",
                        "rec1kugAm2CjV8CYv",
                        "rec9BSqxOdGyfZMPj"
                    ],
                    "Email": "testmentor1@gmail.com",
                    "Code of Conduct Accepted?": true,
                    "Guidebook Read?": true
                }
            },
            {
                "fields": {
                    "Slack Name": "testmentor2",
                    "Full Name": "test2",
                    "Skillsets": [
                        "Javascript",
                        "Java"
                    ],
                    "Mentor Request": [
                        "recoBKojRrxR1rS2t",
                        "reczC78k3vV7p9G0R",
                        "recDAcuRI6f8AICP0",
                        "recsTskf3WmVzzPOP",
                        "rec40FyPUkbPIva7A",
                        "recnjpUNmv5UQ10ma"
                    ],
                    "Email": "abanthes@gmail.com"
                }
            }
        ]
    }
    staging_mentors_table.batch_insert(records)
    print('worked')

    return staging_mentors_table


insert_all_users_to_staging_mentors_table(base_id, table_name)
