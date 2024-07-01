from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate_property"
    
    
    
    def property_sold(self):
        print("In over ride")
        # self.env['account.move'].create({'partner_id': self.partner_id, 'move_type': 'out_invoice', 'journal_id': ''})
        self.env['account.move'].create(
            {
                'journal_id': self.id, 
                'partner_id': self.partner_id.id, 
                'move_type': 'out_invoice',
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06 + 100,
                        }
                    )
                ],
             }
            )
        return super().property_sold()