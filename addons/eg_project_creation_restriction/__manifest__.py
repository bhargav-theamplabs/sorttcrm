{
    'name': 'Project Creation Restriction',
    'version': '16.0.1.0.0',
    'category': 'Project',
    'summery': 'This app will apply restriction on project creation.',
    'author': 'INKERP',
    'website': "http://www.INKERP.com",
    'depends': ['project','crm','task_check_list','project_timeline','web'],

    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/crm_lead_project_views.xml'
    ],

    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': True,
}