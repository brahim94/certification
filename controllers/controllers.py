# -*- coding: utf-8 -*-
# from odoo import http


# class Attestation(http.Controller):
#     @http.route('/attestation/attestation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/attestation/attestation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('attestation.listing', {
#             'root': '/attestation/attestation',
#             'objects': http.request.env['attestation.attestation'].search([]),
#         })

#     @http.route('/attestation/attestation/objects/<model("attestation.attestation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('attestation.object', {
#             'object': obj
#         })
