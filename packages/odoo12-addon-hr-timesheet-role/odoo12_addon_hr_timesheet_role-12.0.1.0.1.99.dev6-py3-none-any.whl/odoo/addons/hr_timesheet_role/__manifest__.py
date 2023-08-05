# Copyright 2018-2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Task Logs by Role',
    'version': '12.0.1.0.1',
    'category': 'Human Resources',
    'website': 'https://github.com/OCA/hr-timesheet',
    'author':
        'Brainbean Apps, '
        'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'summary': 'Track time on project according to the role assigned',
    'depends': [
        'hr_timesheet',
        'project_role',
    ],
    'data': [
        'views/account_analytic_line.xml',
        'views/project_task.xml',
        'views/project_project.xml',
        'views/project_portal_templates.xml',
        'views/res_config_settings.xml',
        'report/report_timesheet_templates.xml',
    ],
}
