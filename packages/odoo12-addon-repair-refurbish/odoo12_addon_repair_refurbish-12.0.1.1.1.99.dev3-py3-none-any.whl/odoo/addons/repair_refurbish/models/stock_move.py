# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models, api


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.model_create_multi
    def create(self, vals_list):
        if 'force_refurbish_location_dest_id' in self.env.context:
            for vals in vals_list:
                vals['location_dest_id'] = self.env.context[
                    'force_refurbish_location_dest_id']
        return super().create(vals_list)
