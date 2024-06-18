
from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Properties"
    # _order = "sequence"
    
    
    active = fields.Boolean('Active', default=False)
    
    name = fields.Char('Title', required=True)
    description = fields.Text('Description', required=True)
    postcode = fields.Char('Post Code', required=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', required=False, readonly=True, copy=False)
    
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Areas (sqm)', default=0)
    facades = fields.Integer('Facades', default=0)
    garden_area = fields.Integer('Garden Area (sqm)', default=0)
    
    garage = fields.Boolean('Garage', default=True)
    garden = fields.Boolean('Garden', default=True)
    
    date_availability = fields.Date('Available From', required=False, copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    
    state = fields.Selection([('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
                             required=True, copy=False)
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'The expected price can\'t be negative.'),
    ]
