from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"
    _order = "sequence, name"
    
    name = fields.Char('Type', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    
    property_ids = fields.One2many("estate.property", "property_type_id")
    
    # offer_ids = fields.One2many(compute="_compute_property_type")
    # offer_ids = fields.One2many(related='property_ids.offer_ids', inverse="property_type_id.offer_ids", store=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', store=True)

    
    
    offer_count = fields.Integer(compute="_compute_offer_count")
    
    @api.depends('property_ids.property_type_id')
    def _compute_property_type(self):
        for record in self:
            record.offer_ids = record.property_ids.property_type_id
            
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)