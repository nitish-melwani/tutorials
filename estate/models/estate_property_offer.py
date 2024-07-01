from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"
    
    
    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute="_compute_date_deadline", inverse="_inverse_date_deadline", readonly=False)
    
    # property_type_id = fields.Many2one(compute="_compute_property_type")
     
    # property_type_id = fields.Many2one("estate.property", related='property_id.property_type_id', inverse='offer_ids', store=True)
    property_type_id = fields.Many2one("estate.property", related='property_id.property_type_id', store=True)
    
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(fields.Date.to_date(record.create_date), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)
            
    # @api.depends('property_id.property_type_id')
    # def _compute_property_type(self):
    #     for record in self:
    #         record.property_type_id = record.property_id.property_type_id
            
            
    @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                created_date = fields.Date.to_date(record.create_date)
            else:
                created_date = fields.Date.today()
            date1 = record.date_deadline
            difference = (date1 - created_date).days
            record.validity = difference
            
    def accept_offer(self):
        for record in self:
            if record.property_id.selling_price:
                raise UserError("Another offer has already been accepted")
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
            record.property_id.state = 'offer accepted'
            record.status = 'accepted'
        return True

    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
    
    
    @api.model
    def create(self, vals):
        record = self.env['estate.property'].browse(vals['property_id'])
        if record.best_price > vals['price']:
            raise UserError("New offer price must be greater than previous offers!")
        if record.expected_price * 0.9 > self.price:
            raise UserError("New offer price must be at least 90% of expected offer price!")
        record.state = 'offer received'
        
        return super(EstatePropertyOffer, self).create(vals)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price >= 0)', 'The offer price can\'t be negative.')
    ]