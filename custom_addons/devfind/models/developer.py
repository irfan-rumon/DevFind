from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re                                                     # Python's regular expression library

class Developer(models.Model):
    _name = 'devfind.developer'
    _description = 'Developer Information'
    _sql_constraints = [
        ('email_unique', 'unique(email)', 'Email must be unique!')
    ]

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    
    technology_ids = fields.Many2many(
        'devfind.technology',
        'tech_dev_mapper_rel',
        'developer_id',
        'technology_id',
        string='Technologies'
    )

    # Add this new computed field
    technologies_list = fields.Char(
        string='Technologies List',
        compute='_compute_technologies_list',
        store=True
    )

    min_hourly_rate = fields.Float(string='Min Hourly Rate', required=True)
    max_hourly_rate = fields.Float(string='Max Hourly Rate', required=True)
    technology_count = fields.Integer(
        string='Technology Count',
        compute='_compute_technology_count'
    )

    @api.depends('technology_ids')
    def _compute_technologies_list(self):
        for record in self:
            record.technologies_list = ', '.join(record.technology_ids.mapped('name'))

    @api.depends('technology_ids')
    def _compute_technology_count(self):
        for record in self:
            record.technology_count = len(record.technology_ids)

    @api.constrains('min_hourly_rate', 'max_hourly_rate')
    def _check_hourly_rates(self):
        for record in self:
            if record.min_hourly_rate > record.max_hourly_rate:
                raise ValidationError("Minimum hourly rate cannot be greater than maximum rate!")

    @api.model
    def create(self, vals):
        # Create user first
        if 'user_id' not in vals:
            user_vals = {
                'name': f"{vals.get('first_name', '')} {vals.get('last_name', '')}",
                'login': vals.get('email'),
                'email': vals.get('email'),
                'groups_id': [(4, self.env.ref('devfind.group_developer').id)],
                'password': vals.get('password'),  # This should be coming from the registration form
            }
            user = self.env['res.users'].create(user_vals)
            vals['user_id'] = user.id
        
        return super(Developer, self).create(vals)