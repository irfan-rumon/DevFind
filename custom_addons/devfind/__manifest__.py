{
    'name': 'devfind',
    'version': '1.0',
    'summary': 'Developer Finding App',  
    'description': 'Module for finding and managing developers', 
    'category': 'Human Resources',  
    'author': 'A S M IRFAN', 
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/developer_views.xml',
        'views/technology_views.xml',
        'views/tech_dev_mapper_views.xml',
    ],
    'installable': True,
    'application': True,
}