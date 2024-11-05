from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Developer(models.Model):
    _name = 'devfind.developer'
    _description = 'Developer Information'
    _sql_constraints = [
        ('email_unique', 'unique(email)', 'Email must be unique!')
    ]

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

    # Computed field to show technology count
    technology_count = fields.Integer(
        string='Technology Count',
        compute='_compute_technology_count'
    )

    @api.depends('technology_ids')
    def _compute_technology_count(self):
        for record in self:
            record.technology_count = len(record.technology_ids)

    @api.constrains('min_hourly_rate', 'max_hourly_rate')
    def _check_hourly_rates(self):
        for record in self:
            if record.min_hourly_rate > record.max_hourly_rate:
                raise ValidationError("Minimum hourly rate cannot be greater than maximum rate!")
