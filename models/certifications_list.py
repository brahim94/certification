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
    employee_name = fields.Char(string="Nom de l'Employer")
    email_id = fields.Char(string="Email")
    state = fields.Selection([
        ('brouillon', 'Brouillion'),
        ('valide', 'Validé'),
        ('envoyer', 'Envoyé'),
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
    
    def send_job_certifica(self):
        template_id = self.env.ref('attestation.job_certifica_email_template').id 
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.state = 'envoyer'

    

    #soft_copy = fields.Binary(string="Soft Copy")
    #file_name = fields.Char(string="File Name") 

    #def send_mail_func(self):
    #    email_template = self.env.ref('module1.test_email_template')
    #    attachment = {
    #        'name': str(self.file_name),
    #        'datas': self.binary_field_name,
    #        'datas_fname': self.file_name,
    #        'res_model': 'job.certifica',
    #         'type': 'binary'
    #        }
    #    id = self.env['ir.attachment'].create(attachment)
    #    email_template.attachment_ids = [(4, ir_id.id)]
    #    email_template.send_mail(self.id, raise_exception=False, force_send=True)
    #    email_template.attachment_ids = [(3, ir_id.id)]