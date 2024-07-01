from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    
    
    def property_sold(self):
        print("In over ride")
        self.env['account.move'].create(
            {
                'journal_id': 1,
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