from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re                                                     # Python's regular expression library

class Developer(models.Model):
    _name = 'devfind.developer'
    _description = 'Developer Information'
    _inherits = {'res.users': 'user_id'}  # Inherit from res.users
    
    # Link to res.users
    user_id = fields.Many2one(
        'res.users', 
        string='Related User', 
        required=True, 
        ondelete='cascade', 
        auto_join=True
    )
    
    # Personal Information
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(compute='_compute_full_name', store=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', required=True)
    
    # Contact Information
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone')
    
    # Professional Information
    technology_ids = fields.Many2many(
        'devfind.technology',
        'tech_dev_mapper_rel',
        'developer_id',
        'technology_id',
        string='Technologies'
    )
    technologies_list = fields.Char(
        string='Technologies List',
        compute='_compute_technologies_list',
    )
    min_hourly_rate = fields.Float(string='Min Hourly Rate', required=True)
    max_hourly_rate = fields.Float(string='Max Hourly Rate', required=True)
    github_profile = fields.Char(string='GitHub Profile')
    linkedin_profile = fields.Char(string='LinkedIn Profile')
    
    _sql_constraints = [
        ('email_unique', 'unique(email)', 'Email must be unique!')
    ]
    
    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"
    
    @api.depends('technology_ids')
    def _compute_technologies_list(self):
        for record in self:
            record.technologies_list = ', '.join(record.technology_ids.mapped('name'))
    
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError("Please enter a valid email address!")
    
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