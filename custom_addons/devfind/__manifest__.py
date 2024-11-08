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
        'views/technology_views.xml',
        'views/menus.xml'
    ],
   
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}