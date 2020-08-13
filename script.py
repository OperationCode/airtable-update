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
    records = [{
        'id': 'rec2NUzgTvbv5RPYr',
        'fields': {
              'Slack Name': 'VetAlly',
            'Full Name': 'Rosendo Gonzalez',
            'Skillsets': ['Resume Reviews', 'General Career Advice'],
            'Max Mentees': 23,
            'Mentor Request': ['recufZzm1LjdiKy3Z'],
            'Email': 'rosendo.gonzalez@gmail.com'},
        'createdTime': '2018-11-24T20:38:25.000Z'
    },
        {
        'id': 'rec425V9c8DsQKckC',
        'fields': {
            'Slack Name': 'vincent',
            'Full Name': 'Vincent Abruzzo',
            'Skillsets': ['React', 'SQL', 'Functional Programming', 'Resume Reviews', 'Career Advice', 'Code Review', 'Web Development (Front-end)', 'Web Development (Back-end)', 'DevOps', 'Linux'],
            'Active': True,
            'Mentor Request': ['recYqfOo2kMC2PDgn', 'recHRSRsEjVtcJ6nC', 'recyWlXUxQLBk9jAW', 'recO6oOcaoWC44ESY'],
            'Email': 'vgabruzzo@gmail.com'
        },
        'createdTime': '2018-03-24T19:14:07.000Z'
    }]
    staging_mentors_table.batch_insert(records)
    print('worked')

    return staging_mentors_table


insert_all_users_to_staging_mentors_table(base_id, table_name)
