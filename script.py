import os
import settings
from airtable import Airtable

mentors_table = os.environ.get('AIRTABLE_MENTORS')
mentees_table = os.environ.get('AIRTABLE_MENTEES')

staging_base_id = os.environ.get('AIRTABLE_STAGING_BASE_ID')
staging_mentors_table = Airtable(staging_base_id, mentors_table)
staging_mentees_table = Airtable(staging_base_id, mentees_table)

production_base_id = os.environ.get('AIRTABLE_PRODUCTION_BASE_ID')
production_mentors_table = Airtable(production_base_id, mentors_table)
production_mentees_table = Airtable(production_base_id, mentees_table)

# MUST CREATE MENTOR REQUEST LINK (but has link to mentors copy table)
# MUST CREATE SERVICES LINK (mentors mentor request mentors copy)
def link_production_mentees_to_mentors(base, table):
    '''
    Creates a dictionary that links mentee Slack username with
    their mentor's email address from production. Returns:

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
            mentor_email = next(
                (mentor['fields']['Email']
                 for mentor in all_mentors if mentor['id'] == assigned[0]),
                None)

            # create the key/value pair in link_dict
            link_dict[all_mentees[mentee]['fields']
                      ['Slack User']] = mentor_email

    return link_dict


link_production_mentees_to_mentors(production_base_id, mentees_table)

# 1. get all records from production mentors table


def get_all_users_from_production_mentors_table(base, table):
    mentors = production_mentors_table.get_all()
    return mentors


# 2. update staging data


def insert_all_users_to_staging_mentors_table(base, table):

    all_users = staging_mentors_table.get_all()
    production_records = get_all_users_from_production_mentors_table(
        production_base_id, mentors_table)

    # remove id from production_records
    replacement_records = [
        production_records[user]['fields']
        for user in range(len(production_records))
    ]

    # remove all linked columns in replacement_records + 'Squads' column
    for mentor in replacement_records:
        if 'Assigned Mentees' in mentor.keys():
            del mentor['Assigned Mentees']
        if 'Mentor Request' in mentor.keys():
            del mentor['Mentor Request']
        if 'Services' in mentor.keys():
            del mentor['Services']
        if 'Squads' in mentor.keys():
            del mentor['Squads']

    # if records exist, delete all records using batch_delete(), then replace
    if len(all_users):
        records_to_delete = [
            all_users[user]['id'] for user in range(len(all_users))
        ]
        staging_mentors_table.batch_delete(records_to_delete)

    staging_mentors_table.batch_insert(replacement_records)

    # RUNS INTO AN ERROR HERE BECAUSE ASSIGNED MENTEE'S RECORD IDS HAVE ALL CHANGED
    # go back through dictionary and link back all the records
    # get id from

    print('worked')

    return staging_mentors_table


insert_all_users_to_staging_mentors_table(staging_base_id, mentors_table)
# 3. update staging data with linkages
# '''
# loops on loops

# for mentor in range(len(replacement_records)):

#         if 'Mentor Assigned' in mentor.keys():
#             # creates a list of record ids for each mentor assigned to a mentee
#             assigned = all_mentees[mentee]['fields']['Mentor Assigned']

#             # use generator to find corresponding record in mentors table
#             mentor_email = next(
#                 (mentor['fields']['Email']
#                  for mentor in all_mentors if mentor['id'] == assigned[0]),
#                 None)

#             # create the key/value pair in link_dict
#             link_dict[all_mentees[mentee]['fields']
#                       ['Slack User']] = mentor_email
# '''
