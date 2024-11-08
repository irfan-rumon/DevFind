{
    'name': 'devfind',
    'version': '1.0',
    'summary': 'Developer Finding Platform',  
    'description': 'Module for finding and managing developers', 
    'category': 'Services',  
    'author': 'A S M IRFAN', 
    'depends': ['base'],
    'data': [
         # Load security first
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        # Then load views
        'views/auth_templates.xml',
        'views/developer_views.xml',
        'views/developer_templates.xml',
        'views/technology_views.xml',
        'views/menus.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'devfind/static/src/components/developer_list/developer_list.js',
            'devfind/static/src/components/developer_list/developer_list.xml',
            'devfind/static/src/components/developer_list/developer_list.scss',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}