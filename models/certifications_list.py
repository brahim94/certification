# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import datetime


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
    date_hire = fields.Date(string="Date d'embauche")
    state = fields.Selection([
        ('brouillon', 'Brouillion'),
        ('valide', 'Validé'),
        ('envoyer', 'Envoyé'),
        ], setting='State', readonly=True, default='brouillon') 
    
    #def _get_default_email(self):
        #return self.env['hr.employee'].search([('name', '=', 'work_email')], limit=1).id

    #email_id = fields.Many2one('hr.employee', string='Email', default=_get_default_email, domain=[('name', '=', 'work_email')])
    
    #@api.onchange('employee_id')
    #def onchange_email_id(self):
        #self.email_id = self.employee_id.work_email
        
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
    
    @api.onchange('employee_id')
    def onchange_email_id(self):
        self.email_id = self.employee_id.work_email
    #def _get_default_hire(self):
        #return self.env['hr.contract'].search([('name', '=', 'date_start')], limit=1).id

    #date_hire = fields.Many2one('hr.contract', string="date d'embauche", default=_get_default_hire, domain=[('name', '=', 'date_start')])
    
    @api.onchange('employee_id')
    def onchange_hire_id(self):
        self.date_hire = self.contrat.date_start 
    
    def _get_default_manager(self):
        return self.env['hr.employee'].search([('name', '=', 'parent_id')], limit=1).id

    manager = fields.Many2one('hr.employee', string='Manager', default=_get_default_manager, domain=[('name', '=', 'parent_id')])
    
    @api.onchange('employee_id')
    def onchange_manager(self):
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

    @api.onchange('employee_id')
    def onchange_email_id(self):
        self.email_id = self.employee_id.work_email

    def _get_default_contrat(self):
        return self.env['hr.contract'].search([], limit=1).id

    contrat = fields.Many2one('hr.contract', string='Contrat', default=_get_default_contrat, domain=[])
    
    @api.onchange('employee_id')
    def onchange_contrat_id(self):
        self.contrat = self.employee_id.contract_id 

    @api.onchange('employee_id')
    def onchange_hire_id(self):
        self.hire = self.contrat.date_start

    @api.onchange('employee_id')
    def onchange_wage_id(self):
        self.amount_money = self.contrat.wage

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
    demand_date = fields.Datetime(string="Date demande")
    send_date = fields.Datetime(string="Date envoi")
    write_date = fields.Date(string='Write Date')
    months_number = fields.Integer(string='N° Mois')
    name_bank = fields.Char(string='Banque')
    name_agency = fields.Char(string='Agence')
    rib_number = fields.Char(string='N° RIB')
    state = fields.Selection([
    ('brouillon', 'Brouillion'),
    ('valide', 'Validé'),
    ('envoyer', 'Envoyé'),
    ], setting='State', readonly=True, default='brouillon')

    #@api.depends('demand_date')
    #def _get_month(self):
        #month = datetime.strptime(self.demand_date, '%Y-%m-%d').strftime('%m')
        #for record in self:
            #record['months_number'] = datetime.strftime(datetime.strptime(demand_date, "%Y-%m-%d"))

    def _get_default_manager(self):
        return self.env['hr.employee'].search([('name', '=', 'parent_id')], limit=1).id

    manager = fields.Many2one('hr.employee', string='Manager', default=_get_default_manager, domain=[('name', '=', 'parent_id')])
    
    @api.onchange('employee_id')
    def onchange_manager_id(self):
        self.manager = self.employee_id.parent_id

    @api.onchange('employee_id')
    def onchange_email_id(self):
        self.email = self.employee_id.work_email

    def _get_default_contrat(self):
        return self.env['hr.contract'].search([], limit=1).id

    contrat = fields.Many2one('hr.contract', string='Contrat', default=_get_default_contrat, domain=[])
    
    @api.onchange('employee_id')
    def onchange_contrat_id(self):
        self.contrat = self.employee_id.contract_id 

    #@api.onchange('employee_id')
    #def onchange_rib_id(self):
        #self.rib_number = self.contrat.bank_account_id 
    
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

    #def _get_month(self, date):
        #"""Get month from date"""
        #return datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%m")    
        #self.month = _get_month(self.date)


class leave_certification(models.Model):
    _name = 'leave.certifica'
    _description = 'Attestation de congé Model'

    name = fields.Char(string='Certifica leave Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    company_id = fields.Many2one(
    'res.company',
    'Company',
    default=lambda self: self.env['res.company']._company_default_get('attestation')
    )
    employee_id = fields.Many2one('hr.employee', string="Employee")
    email_id = fields.Char(string="Email")
    write_date = fields.Date(string='Write Date')
    cnss_number = fields.Char(string='C.N.S.S. N°')
    leave_date_start = fields.Date(string="Début de congé")
    leave_date_end = fields.Date(string="Fin de congé")
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

    @api.onchange('employee_id')
    def onchange_email_id(self):
        self.email_id = self.employee_id.work_email

    @api.model 
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('leave.order') or ('New')
        result = super(leave_certification, self).create(vals)
        return result 

    def action_validate_leave(self):
        for rec in self:
            rec.state = 'valide'

    def print_leave(self):
        return self.env.ref('attestation.action_report_leave').report_action(self)

    def send_leave_certifica(self):
        template_id = self.env.ref('attestation.leave_certifica_email_template').id 
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.state = 'envoyer' 


class work_certification(models.Model):
    _name = 'work.certifica'
    _description = 'Model Certifat de travail'

    name = fields.Char(string='Certifica work Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    company_id = fields.Many2one(
    'res.company',
    'Company',
    default=lambda self: self.env['res.company']._company_default_get('attestation')
    )
    employee_id = fields.Many2one('hr.employee', string="Employee")
    email_id = fields.Char(string="Email")
    write_date = fields.Date(string='Write Date')
    cnss_number = fields.Char(string='C.N.S.S. N°')
    date_hire = fields.Date(string="Date d'embauche")
    date_leave = fields.Date(string="Date de départ")
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

    def _get_default_manager(self):
        return self.env['hr.employee'].search([('name', '=', 'parent_id')], limit=1).id

    manager = fields.Many2one('hr.employee', string='Manager', default=_get_default_manager, domain=[('name', '=', 'parent_id')])
    
    @api.onchange('employee_id')
    def onchange_manager_id(self):
        self.manager = self.employee_id.parent_id

    @api.onchange('employee_id')
    def onchange_hire_id(self):
        self.date_hire = self.contrat.date_start

    @api.onchange('employee_id')
    def onchange_leave_id(self):
        self.date_leave = self.contrat.date_end

    def _get_default_job(self): 
        return self.env['hr.job'].search([], limit=1).id

    fiche_poste = fields.Many2one('hr.job', string='Fiche de poste', default=_get_default_job, domain=[])
    
    @api.onchange('employee_id')
    def onchange_id(self):
        self.fiche_poste = self.employee_id.job_id

    @api.onchange('employee_id')
    def onchange_email_id(self):
        self.email_id = self.employee_id.work_email

    @api.model 
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('work.order') or ('New')
        result = super(work_certification, self).create(vals)
        return result 

    def action_validate_work(self):
        for rec in self:
            rec.state = 'valide'

    def print_work(self):
        return self.env.ref('attestation.action_report_work').report_action(self)

    def send_work_certifica(self):
        template_id = self.env.ref('attestation.work_certifica_email_template').id 
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.state = 'envoyer'  


class notify_certification(models.Model):
    _name = 'notify.certifica'
    _description = 'Model Notification de départ'

    name = fields.Char(string='Certifica notify Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    company_id = fields.Many2one(
    'res.company',
    'Company',
    default=lambda self: self.env['res.company']._company_default_get('attestation')
    )
    employee_id = fields.Many2one('hr.employee', string="Employee")
    email_id = fields.Char(string="Email")
    write_date = fields.Date(string='Write Date')
    cin_number = fields.Char(string='CIN N°')
    date_hire = fields.Date(string="Date d'embauche")
    date_leave = fields.Date(string="Date de départ")
    name_bank = fields.Char(string='Banque')
    name_agency = fields.Char(string='Agence')
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

    def _get_default_manager(self):
        return self.env['hr.employee'].search([('name', '=', 'parent_id')], limit=1).id

    manager = fields.Many2one('hr.employee', string='Manager', default=_get_default_manager, domain=[('name', '=', 'parent_id')])
    
    @api.onchange('employee_id')
    def onchange_fuel_product_id(self):
        self.manager = self.employee_id.parent_id

    @api.onchange('employee_id')
    def onchange_email_id(self):
        self.email_id = self.employee_id.work_email
        
    @api.model 
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('notify.order') or ('New')
        result = super(notify_certification, self).create(vals)
        return result 

    def action_validate_notify(self):
        for rec in self:
            rec.state = 'valide'

    def print_notify(self):
        return self.env.ref('attestation.action_report_notify').report_action(self)

    def send_notify_certifica(self):
        template_id = self.env.ref('attestation.notify_certifica_email_template').id 
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.state = 'envoyer'
