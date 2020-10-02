import os
import settings
from airtable import Airtable

mentors_table = os.environ.get('AIRTABLE_MENTORS')
mentees_table = os.environ.get('AIRTABLE_MENTEES')
skillsets_table = os.environ.get('AIRTABLE_SKILLSETS')

staging_base_id = os.environ.get('AIRTABLE_STAGING_BASE_ID')
staging_mentors_table = Airtable(staging_base_id, mentors_table)
staging_mentees_table = Airtable(staging_base_id, mentees_table)
staging_skillsets_table = Airtable(staging_base_id, skillsets_table)

production_base_id = os.environ.get('AIRTABLE_PRODUCTION_BASE_ID')
production_mentors_table = Airtable(production_base_id, mentors_table)
production_mentees_table = Airtable(production_base_id, mentees_table)
production_skillsets_table = Airtable(production_base_id, skillsets_table)

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


def insert_all_users_to_staging_mentors_table(base, table):
    '''
    Removes record ids, linked columns (Assigned Mentees, Mentor
    Request, and Services), and column 'Squads' from production
    records in 'Mentors' table.

    Deletes all records from 'Mentors' table in staging.

    Inserts production records into 'Mentors' table in staging.
    '''

    all_users = staging_mentors_table.get_all()
    production_records = production_mentors_table.get_all()

    # remove id from production_records to get only the records
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
        # gets record ids to use in batch_delete()
        records_to_delete = [
            all_users[user]['id'] for user in range(len(all_users))
        ]
        staging_mentors_table.batch_delete(records_to_delete)

    staging_mentors_table.batch_insert(replacement_records)

    # print('inserted all replacement_records into staging')

    return staging_mentors_table


# insert_all_users_to_staging_mentors_table(staging_base_id, mentors_table)


# 3. update staging data with linkages
'''
loops on loops

for mentor in range(len(replacement_records)):

        if 'Mentor Assigned' in mentor.keys():
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
'''


def copies_production_skillsets_to_staging(base, table):
    '''
    Get all skills from production 'Skillsets' table.
    Delete all skills from staging 'Skillsets' table.
    Insert all skills from production 'Skillsets' to staging 'Skillsets'.
    '''

    production_skills = production_skillsets_table.get_all()
    skills_to_delete = staging_skillsets_table.get_all()

    # get only the fields from each record (removing the old ids)
    skills_to_add = [
        production_skills[skill]['fields']
        for skill in range(len(production_skills))
    ]

    # check if staging 'skillsets' table has records, then delete all
    if len(skills_to_delete):
        # get the record id to use in .batch_delete()
        records_to_delete = [
            skills_to_delete[skill]['id']
            for skill in range(len(skills_to_delete))
        ]
        staging_skillsets_table.batch_delete(records_to_delete)

    staging_skillsets_table.batch_insert(skills_to_add)

    # print('inserted all production skills into staging')

    return staging_skillsets_table


# copies_production_skillsets_to_staging(staging_base_id, skillsets_table)
