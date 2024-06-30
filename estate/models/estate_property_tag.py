from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    
    name = fields.Char('Tag', required=True)
    color = fields.Integer('Color')
    
    _sql_constraints = [
        ('check_property_tags', 'UNIQUE (name)', 'Property tags must be unique'),
    ]