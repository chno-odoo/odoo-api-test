from Odoo import Odoo
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    url = os.getenv('ODOO_URL')
    db = os.getenv('ODOO_DB')
    username = os.getenv('ODOO_USERNAME')
    api_key = os.getenv('ODOO_API_KEY')

    odoo = Odoo(url, db, username, api_key)

    # Prompt the user for input
    user_name = input("Please enter the Odoo username (ex. chno@odoo.com): ")
    project_name = input("Please enter the project name (ex. Help): ")

    # Search for the user ID by login
    user_data = odoo.searchRead('res.users', [('login', '=', user_name)], {'fields': ['id']})
    if not user_data:
        print(f'User {user_name} not found.')
        exit()
    user_id = user_data[0]['id']

    # Search for the project ID by name
    project_data = odoo.searchRead('project.project', [('name', '=', project_name)], {'fields': ['id']})
    if not project_data:
        print(f'Project {project_name} not found.')
        exit()
    project_id = project_data[0]['id']

    # Search for tasks assigned to the user within the project
    tasks = odoo.searchRead('project.task', [
        ('project_id', '=', project_id),
        ('user_ids', 'in', user_id)
    ], {'fields': ['id']})

    print(f'Number of tasks assigned to {user_name} in project {project_name}: {len(tasks)}')
