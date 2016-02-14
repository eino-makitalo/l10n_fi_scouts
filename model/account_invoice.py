#--*-- coding: utf-8 --*--
from openerp import models, fields, api
# noinspection PyProtectedMember
from openerp.tools.translate import _
import re
import logging

log = logging.getLogger(__name__)
from openerp.exceptions import ValidationError

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    kuksa_number = fields.Char(string="Kuksa Invoice",
                               help="Kuksa Invoice number",
                               states={'draft': [('readonly', False)]},
                               readonly=True,
                               size=10)

    def _justnumbers(self):
        for record in self:
            if record.kuksa_number:
                record.kuksa_int  = int("0" +''.join(c for c in record.kuksa_number if c.isdigit()))
    
    kuksa_int=fields.Integer(string="Kuksa",help="Kuksa invoice number 0=if not in Kuksa",compute=_justnumbers)

    @api.constrains("kuksa_number")
    def _checknum(self):
        for rec in self:
            if rec.kuksa_number and (not rec.kuksa_number.isdigit()):
                raise ValidationError("Kuksa-laskun pitää olla numero")
    
    @api.depends("kuksa_number")
    def _showlink(self):
        for rec in self:
            if rec.kuksa_number:
                kn=int(rec.kuksa_number)
                if  kn>0:
                    rec.kuksa_link="https://kuksa.partio.fi/Taloushallinto/Myyntireskontra.aspx?MinLaskunumero=%d&MaxLaskunumero=%d" % (kn,kn)                
                    
    def _formatref():
        def _formatref(callback,val01):
            return val01
        
    kuksa_link = fields.Char(string="Kuksa",compute=_showlink,help="Link to Kuksa system", translate=_formatref)
    _sql_constraints = [
        ('kuksa_number_must_be_unqiue', 'unique(kuksa_number)', 'Kuksa invoice number must be unique. Check the number.'),
    ]    
    