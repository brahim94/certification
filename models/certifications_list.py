# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class Job_Certification(models.Model):
    _name = 'job.certifica'
    _description = 'Attestation Travail Model'

    name = fields.Char(string='Certifica Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    company_name = fields.Char(string='Nom de la société')
    cnss_number = fields.Integer(string='C.N.S.S. N°')
    write_date = fields.Datetime(string='Write Date')
    hire_date = fields.Date(string="Date d'embauche")
    occupied_job = fields.Char(string="Fiche de poste")
    manager = fields.Char(string="Nom du responsable")
    state = fields.Selection([
        ('brouillon', 'Brouillion'),
        ('valide', 'Validé'),
        ('envoyer', 'Envoyer'),
        ], setting='State', readonly=True, default='brouillon')
    
    @api.model 
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('job.order') or ('New')
        result = super(Job_Certification, self).create(vals)
        return result 

    def action_validate(self):
        for rec in self:
            rec.state = 'valide'
    
    def print_job(self):
        return self.env.ref('attestation.action_report_job').report_action(self)