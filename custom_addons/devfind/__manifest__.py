{
    'name': 'devfind',
    'version': '1.0',
    'summary': 'Developer Finding App',  
    'description': 'Module for finding and managing developers', 
    'category': 'Human Resources',  
    'author': 'A S M IRFAN', 
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/developer_views.xml'
    ],
    'installable': True,
    'application': True,
}