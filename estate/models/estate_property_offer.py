from odoo import api, fields, models
from datetime import datetime

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    
    
    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute="_compute_date_deadline", inverse="_inverse_date_deadline", readonly=False)
    
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(fields.Date.to_date(record.create_date), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)
            
            
    @api.depends('create_date', 'date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                created_date = fields.Date.to_date(record.create_date)
            else:
                created_date = fields.Date.today()
            date1 = record.date_deadline
            difference = (date1 - created_date).days
            record.validity = difference
