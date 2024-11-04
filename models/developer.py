from odoo import models, fields

class Developer(models.Model):
    _name = 'devfind.developer'
    _description = 'Developer Information'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    
    # Many2many field to link developers with their technologies/skills
    technology_ids = fields.Many2many(
        'devfind.technology',   # model name to link
        'tech_dev_mapper_rel',  # name of the relation table
        'developer_id',         # field for developer ID
        'technology_id',        # field for technology ID
        string='Technologies'   # label for the field
    )

    min_hourly_rate = fields.Float(string='Min Hourly Rate', required=True)
    max_hourly_rate = fields.Float(string='Max Hourly Rate', required=True)
