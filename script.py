import os
import settings
from airtable import Airtable

table_name = os.environ.get('AIRTABLE_TABLE_NAME')
mentors_table = os.environ.get('AIRTABLE_MENTORS')
mentees_table = os.environ.get('AIRTABLE_MENTEES')

staging_base_id = os.environ.get('AIRTABLE_STAGING_BASE_ID')
staging_mentors_table = Airtable(staging_base_id, mentors_table)
staging_mentees_table = Airtable(staging_base_id, mentees_table)

production_base_id = os.environ.get('AIRTABLE_PRODUCTION_BASE_ID')
production_mentors_table = Airtable(production_base_id, mentors_table)
production_mentees_table = Airtable(production_base_id, mentees_table)


# 1. get all records from production mentors table
'''
put the data into the dictionary and remove from table at the same time
use a pop-type function if possible

mentor = staging_record.mentor
delete(staging_record.mentor)

mentor = staging_record.mentor.pop()

link_dict[staging_record.name] = mentor

'''


def get_all_users_from_production_mentees_table(base, table):
    '''
    Creates a dictionary that links mentee Slack username with
    their mentor's email address. Returns:

        {
            'username': 'mentor1@email.com',
            'mentee_2': 'mentor2@email.com'
        }
    '''

    all_mentors = production_mentors_table.get_all()
    all_mentees = production_mentees_table.get_all()
    link_dict = {}

    # generate dictionary for linking mentee to mentor

    for mentee in range(len(all_mentees)):
        mentee_fields = all_mentees[mentee]['fields']

        if 'Mentor Assigned' in mentee_fields.keys():
            # creates a list of record ids for each mentor assigned to a mentee
            assigned = all_mentees[mentee]['fields']['Mentor Assigned']
            
            # use generator to find corresponding record in mentors table
            mentor_email = next((mentor['fields']['Email'] for mentor in all_mentors if mentor['id'] == assigned[0]), None)

            # create the key/value pair in link_dict
            link_dict[all_mentees[mentee]['fields']['Slack User']] = mentor_email

    return link_dict

get_all_users_from_production_mentees_table(production_base_id, mentees_table)

# 2. update staging data
'''
just post
'''

# 3. update staging data with linkages
'''
loops on loops
'''


# def insert_all_users_to_staging_mentors_table(base, table):

#     all_users = staging_mentors_table.get_all()
#     production_records = get_all_users_from_production_mentors_table(production_base_id, table_name)
    
#     # create new dictionary
#     # take it out of production_record and put into dictionary

#     # remove id from production_records and remove mentees assigned (but still store it in a dictionary)
#     # ISSUE: THE ASSIGNED MENTEES' RECORD IDS HAVE ALSO ALL CHANGED
#     replacement_records = [production_records[user]['fields'] for user in range(len(production_records))]

#     # if records exist, delete all records using batch_delete(), then replace

#     if len(all_users):
#         records_to_delete = [all_users[user]['id'] for user in range(len(all_users))]
#         staging_mentors_table.batch_delete(records_to_delete)
    
#     # RUNS INTO AN ERROR HERE BECAUSE ASSIGNED MENTEE'S RECORD IDS HAVE ALL CHANGED
#     # make dictionary from mentor request table {record_id: slack_username??}
#     # figure out how to create records without the links - maybe async
#     # look up in dictionary the id of new record
#     # BUT even the mentor request table is linked back to the original table
#     staging_mentors_table.batch_insert(replacement_records)

#     # go back through dictionary and link back all the records
#     # get id from 

    
#     print('worked')

#     return staging_mentors_table


# insert_all_users_to_staging_mentors_table(staging_base_id, table_name)
