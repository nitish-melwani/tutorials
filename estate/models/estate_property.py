
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Properties"
    _order = "id desc"
    
    
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
    garden_orientation = fields.Selection([('', ''), ('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    
    state = fields.Selection([('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
                             required=True, copy=False, default='new')
    
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    
    user_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user.id)
    # user_id = fields.Many2one("estate.sales.person", string="Seller", default=lambda self: self.env.user.id)
    
    property_tags = fields.Many2many("estate.property.tag", string="Property Tag")
    
    offer_ids =  fields.One2many("estate.property.offer", "property_id")
    
    total_area = fields.Integer('Total Area (sqm)', compute="_compute_total_area")
    
    best_price = fields.Float('Best Offer', compute="_compute_best_price")
    
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            list_prices = record.mapped('offer_ids.price')
            if len(list_prices) > 0:
                record.best_price = max(list_prices)
            else:
                record.best_price = 0
            
    @api.onchange("garden")
    def _onchange_garden(self):
        if(self.garden):
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
            
    def property_sold(self):
        for record in self:
            print(record.state)
            if record.state == 'canceled':
                raise UserError("Canceled property cannot be sold")
            else:
                record.state = 'sold'
        return True

    def property_canceled(self):
        for record in self:
            print(record.state)
            if record.state == 'sold':
                raise UserError("Sold property cannot be canceled")
            else:
                record.state = 'canceled'
        return True
    
    
    @api.constrains('expected_price', 'selling_price')
    def _check_price(self):
        for record in self:
            print(record.selling_price)
            print(record.expected_price)
            if float_is_zero(record.selling_price, precision_digits=2) == False:
                if float_compare(record.selling_price, (record.expected_price * 0.9), precision_digits=2) < 0:
                    raise ValidationError("Selling price must be at least 90 % of expected price")
                
                
    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_acrive(self):
        if any(record.state in ['offer received', 'offer accepted', 'sold'] for record in self):
            raise UserError("Can only delete a new or cancelled property!")
    
        
        
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'The expected price can\'t be negative.'),
        ('check_selling_price', 'CHECK(selling_price >= 0 OR selling_price is Null)', 'The selling price can\'t be negative.'),
    ]
