from odoo import models, fields, api

class Technology(models.Model):
    _name = 'devfind.technology'
    _description = 'Technology Information'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Technology name must be unique!')
    ]

    name = fields.Char(string='Technology Name', required=True)
    developer_ids = fields.Many2many(
        'devfind.developer',
        'tech_dev_mapper_rel',  # Same table name as in Developer model
        'technology_id',
        'developer_id',
        string='Developers'
    )