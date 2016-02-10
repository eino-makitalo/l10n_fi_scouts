#--*-- coding: utf-8 --*--

from openerp import models, fields, api
# noinspection PyProtectedMember
from openerp.tools.translate import _
import re
import logging

from checkref import calc_checksum
from openerp.exceptions import ValidationError


log = logging.getLogger(__name__)

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    member_id = fields.Char(string="Member id",help="Member id from Kuksa-system (or customer id for non-scouts)")
    # copy code - ugly start
    def _formatref(callback,val01):
        if val01:
            val01=val01.replace(u' ','')            
            if len(val01)>5:
                palat=[val01[i:i+5] for i in range(0, len(val01), 5)]
                return " ".join(palat)  # Recommended format for ref number 
        return val01


    @api.depends('ref_number')
    def _clean_refnum(self):
        for record in self:
            if record.ref_number:
                record.ref_number_clean=record.ref_number.replace(' ','')

    @api.constrains('ref_number')
    def _checkref(self):
        errmsg=None
        try:
            for record in self:
                if record.ref_number==False:
                    return
                if len(record.ref_number.strip())>0:
                    # only numbers and spaces expected
                    val01=self.ref_number.strip()
                    val01=val01.replace(u' ','')
                    if len(val01)<2:
                        errmsg=_("Too short ref number. Smallest possible is 13 (last digit is checksum)")
                    if val01.isdigit():
                        if len(val01)>20:
                            errmsg=_("Ref number can be max 20 digits")
                            return
                        numberpart=val01[:-1]
                        checksum=val01[-1:]
                        checksum_ok = calc_checksum(numberpart)
                        if int(checksum)!=checksum_ok:
                            errmsg=_("Ref number is invalid last digit (checksum) is %d but it should be %d") % (int(checksum),checksum_ok)
                            return 
                    else:
                        errmsg= _("Ref number must be only digits and spaces")
                        return
        finally:
            if errmsg: 
                raise ValidationError(errmsg)

    ref_number = fields.Char(
        string = "Reference Number",
        store=True,
        translate=_formatref,
        help='Fixed reference number for member to pay some extra payments for scout group'
    )

    ref_number_clean = fields.Char(
        'Reference Number without any space',
        store=True,
        compute='_clean_refnum'
    )

    # copy code - ugly end

1
