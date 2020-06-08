# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class Job_Certification(models.Model):
    _name = 'job.certifica'
    _description = 'Attestation Travail Model'

    name = fields.Char(string='Certifica Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    company_id = fields.Many2one(
    'res.company',
    'Company',
    default=lambda self: self.env['res.company']._company_default_get('attestation')
    )
    cnss_number = fields.Char(string='C.N.S.S. N°')
    write_date = fields.Date(string='Write Date')
    demand_date = fields.Datetime(string="Date demande")
    send_date = fields.Datetime(string="Date envoi")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    email_id = fields.Char(string="Email")
    state = fields.Selection([
        ('brouillon', 'Brouillion'),
        ('valide', 'Validé'),
        ('envoyer', 'Envoyé'),
        ], setting='State', readonly=True, default='brouillon') 
    
    def _get_default_contrat(self):
        return self.env['hr.contract'].search([], limit=1).id

    contrat = fields.Many2one('hr.contract', string='Contrat', default=_get_default_contrat, domain=[])
    
    @api.onchange('employee_id')
    def onchange_contrat_id(self):
        self.contrat = self.employee_id.contract_id 

    def _get_default_job(self): 
        return self.env['hr.job'].search([], limit=1).id

    fiche_poste = fields.Many2one('hr.job', string='Fiche de poste', default=_get_default_job, domain=[])
    
    @api.onchange('employee_id')
    def onchange_id(self):
        self.fiche_poste = self.employee_id.job_id
    
    def _get_default_hire(self):
        return self.env['hr.contract'].search([('name', '=', 'date_start')], limit=1).id

    date_hire = fields.Many2one('hr.contract', string="date d'embauche", default=_get_default_hire, domain=[('name', '=', 'date_start')])
    
    @api.onchange('employee_id')
    def onchange_hire_id(self):
        self.date_hire = self.contrat.date_start 
    
    def _get_default_manager(self):
        return self.env['hr.employee'].search([('name', '=', 'parent_id')], limit=1).id

    manager = fields.Many2one('hr.employee', string='Manager', default=_get_default_manager, domain=[('name', '=', 'parent_id')])
    
    @api.onchange('employee_id')
    def onchange_fuel_product_id(self):
        self.manager = self.employee_id.parent_id
    
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

class salary_certification(models.Model):
    _name = 'salary.certifica'
    _description = 'Attestation de salaire Model'

    name = fields.Char(string='Certifica salary Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    company_id = fields.Many2one(
    'res.company',
    'Company',
    default=lambda self: self.env['res.company']._company_default_get('attestation')
    )
    employee_id = fields.Many2one('hr.employee', string="Employee")
    email_id = fields.Char(string="Email")
    write_date = fields.Date(string='Write Date')
    amount_money = fields.Char(string='Salaire brut en Dh')
    hire = fields.Date(string="Date d'embauche")
    salary_date_create = fields.Date(string="Date de paye")
    state = fields.Selection([
    ('brouillon', 'Brouillion'),
    ('valide', 'Validé'),
    ('envoyer', 'Envoyé'),
    ], setting='State', readonly=True, default='brouillon')

    def _get_default_manager(self):
        return self.env['hr.employee'].search([('name', '=', 'parent_id')], limit=1).id

    manager = fields.Many2one('hr.employee', string='Manager', default=_get_default_manager, domain=[('name', '=', 'parent_id')])
    
    @api.onchange('employee_id')
    def onchange_manager_id(self):
        self.manager = self.employee_id.parent_id

    @api.model 
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('salary.order') or ('New')
        result = super(salary_certification, self).create(vals)
        return result 

    def action_validate_salary(self):
        for rec in self:
            rec.state = 'valide'

    def print_salary(self):
        return self.env.ref('attestation.action_report_salary').report_action(self)

    def send_salary_certifica(self):
        template_id = self.env.ref('attestation.salary_certifica_email_template').id 
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.state = 'envoyer'

class domiciliation_certification(models.Model):
    _name = 'domiciliation.certifica'
    _description = 'Attestation de domiciliation Model'

    name = fields.Char(string='Certifica domiciliation Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    company_id = fields.Many2one(
    'res.company',
    'Company',
    default=lambda self: self.env['res.company']._company_default_get('attestation')
    )
    employee_id = fields.Many2one('hr.employee', string="Employee")
    email = fields.Char(string="Email")
    write_date = fields.Date(string='Write Date')
    demand_date = fields.Datetime(string="Date demande")
    send_date = fields.Datetime(string="Date envoi")
    months_number = fields.Integer(string='N° Mois')
    name_bank = fields.Char(string='Banque')
    name_agency = fields.Char(string='Agence')
    rib_number = fields.Char(string='N° RIB')
    state = fields.Selection([
    ('brouillon', 'Brouillion'),
    ('valide', 'Validé'),
    ('envoyer', 'Envoyé'),
    ], setting='State', readonly=True, default='brouillon')

    def _get_default_manager(self):
        return self.env['hr.employee'].search([('name', '=', 'parent_id')], limit=1).id

    manager = fields.Many2one('hr.employee', string='Manager', default=_get_default_manager, domain=[('name', '=', 'parent_id')])
    
    @api.onchange('employee_id')
    def onchange_fuel_product_id(self):
        self.manager = self.employee_id.parent_id

    @api.model 
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('domiciliation.order') or ('New')
        result = super(domiciliation_certification, self).create(vals)
        return result 

    def action_validate_domiciliation(self):
        for rec in self:
            rec.state = 'valide'

    def print_domiciliation(self):
        return self.env.ref('attestation.action_report_domiciliation').report_action(self)

    def send_domiciliation_certifica(self):
        template_id = self.env.ref('attestation.domiciliation_certifica_email_template').id 
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.state = 'envoyer'

    

    