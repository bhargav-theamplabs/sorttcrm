{
    'name': 'Project Creation Restriction',
    'version': '16.0.1.0.0',
    'category': 'Project',
    'summery': 'This app will apply restriction on project creation.',
    'author': 'INKERP',
    'website': "http://www.INKERP.com",
    'depends': ['project','crm'],

    'data': [
        'security/group.xml',
    ],

    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}