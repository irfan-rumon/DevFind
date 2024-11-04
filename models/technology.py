from odoo import models, fields

class Technology(models.Model):
    _name = 'finddev.technology'
    _description = 'Technology Information'

    name = fields.Char(string='Technology Name', required=True)