# -*- coding: utf-8 -*-
{
    'name': 'Tasks Check List',
    'version': '1.0.0',
    'summary': """Checklist for Task Completion""",
    'description': """Evaluate task completion on the basis of checklists""",
    'category': 'Project',
    'author': 'Odoo Mates',
    'company': 'Odoo Mates',
    'maintainer': 'Odoo Mates',
    'website': 'http://odoomates.tech',
    'depends': ['project'],
    'live_test_url': 'https://www.youtube.com/watch?v=bEhhlB2dNT0',
    'data': [
        'data/task.xml',
        'data/task_template.xml',
        'security/ir.model.access.csv',
        'views/project_task_view.xml',
        'views/task_checklist_view.xml',
        'views/milestone_stage_view.xml',
        'views/task_tempalate_view.xml',
    ],
    'demo': [
        'demo/checklist_demo.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': True,
    'application': False,
}
