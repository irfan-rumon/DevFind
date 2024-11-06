from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re                                                     # Python's regular expression library

class Developer(models.Model):
    _name = 'devfind.developer'
    _description = 'Developer Information'
    _sql_constraints = [
        ('email_unique', 'unique(email)', 'Email must be unique!')
    ]

     # Add user_id field (Many2one relationship with res.users)
    user_id = fields.Many2one(
        'res.users',
        string='User',
        ondelete='cascade',  # Automatically delete the developer record if the associated user is deleted
        required=True
    )


    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    name = fields.Char(string="Name", compute='_compute_name', store=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=True)
    password = fields.Char(string="Password", required=True)
    github_profile = fields.Char(string="GitHub Profile")
    linkedin_profile = fields.Char(string="LinkedIn Profile")
    
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

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"

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
        # Create user first if 'user_id' is not provided
        if 'user_id' not in vals:
            user_vals = {
                'name': f"{vals.get('first_name', '')} {vals.get('last_name', '')}",
                'login': vals.get('email'),
                'email': vals.get('email'),
                'groups_id': [(4, self.env.ref('devfind.group_developer').id)],
                'password': vals.get('password'),  # This should be coming from the registration form
            }

            # Create the user record
            user = self.env['res.users'].create(user_vals)

            # Assign the user_id to the developer record
            vals['user_id'] = user.id

            # Proceed with the creation of the developer record
            return super(Developer, self).create(vals)