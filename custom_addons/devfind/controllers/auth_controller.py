from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import werkzeug

class AuthController(http.Controller):
    @http.route('/developer/register', type='http', auth='public', website=True)
    def register_form(self, **kw):
        return request.render('devfind.developer_registration_template', {})

    @http.route('/developer/register/submit', type='http', auth='public', website=True)
    def register_submit(self, **post):
        try:
            # Create the developer
            vals = {
                'first_name': post.get('first_name'),
                'last_name': post.get('last_name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'gender': post.get('gender'),
                'password': post.get('password'),  # Will be hashed by Odoo
                'min_hourly_rate': float(post.get('min_hourly_rate', 0)),
                'max_hourly_rate': float(post.get('max_hourly_rate', 0)),
                'github_profile': post.get('github_profile'),
                'linkedin_profile': post.get('linkedin_profile'),
            }
            
            developer = request.env['devfind.developer'].sudo().create(vals)
            return werkzeug.utils.redirect('/web/login')
        except ValidationError as e:
            return request.render('devfind.developer_registration_template', {
                'error': str(e),
                'values': post,
            })