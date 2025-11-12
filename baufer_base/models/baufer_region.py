# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BauferRegion(models.Model):
    """
    Modelo para gestión de regiones de Chile.

    Permite marcar zonas estratégicas donde BAUFER ofrece cobertura prioritaria.
    15 regiones de Chile con indicadores de cobertura y tipo de zona.
    """
    _name = 'baufer.region'
    _description = 'Región BAUFER'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nombre Región',
        required=True,
        index=True,
        help='Nombre completo de la región (ej: Región de Antofagasta)'
    )

    code = fields.Char(
        string='Código',
        required=True,
        index=True,
        help='Código corto de la región (ej: ANT, ATA)'
    )

    sequence = fields.Integer(
        string='Secuencia',
        default=10,
        help='Orden de visualización (menor primero)'
    )

    country_id = fields.Many2one(
        'res.country',
        string='País',
        required=True,
        default=lambda self: self.env.ref('base.cl', raise_if_not_found=False),
        help='País al que pertenece la región'
    )

    mining_area = fields.Boolean(
        string='Zona Estratégica',
        default=False,
        help='Indica si es una zona estratégica prioritaria para la operación'
    )

    service_coverage = fields.Boolean(
        string='Cobertura Servicio',
        default=True,
        help='Indica si BAUFER tiene cobertura de servicio en esta región'
    )

    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Si está inactivo, la región no se mostrará en selecciones'
    )

    description = fields.Text(
        string='Descripción',
        help='Información adicional sobre la región'
    )

    partner_count = fields.Integer(
        string='Cantidad Clientes',
        compute='_compute_partner_count',
        store=False,
        help='Número de clientes que operan en esta región'
    )

    delivery_count = fields.Integer(
        string='Cantidad Entregas',
        compute='_compute_delivery_count',
        store=False,
        help='Número de entregas realizadas en esta región'
    )

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'El código de región debe ser único!'),
        ('name_uniq', 'unique(name)', 'El nombre de región debe ser único!'),
    ]

    @api.depends('name')
    def _compute_partner_count(self):
        """Calcula la cantidad de clientes por región."""
        for region in self:
            region.partner_count = self.env['res.partner'].search_count([
                ('region_operations', 'in', region.id)
            ])

    @api.depends('name')
    def _compute_delivery_count(self):
        """Calcula la cantidad de entregas por región."""
        for region in self:
            # Este cálculo se completará cuando exista el módulo baufer_sale
            region.delivery_count = 0

    @api.constrains('code')
    def _check_code_uppercase(self):
        """Valida que el código esté en mayúsculas."""
        for region in self:
            if region.code and region.code != region.code.upper():
                raise ValidationError('El código de región debe estar en mayúsculas.')

    def name_get(self):
        """Formato de visualización: [CODE] Name."""
        result = []
        for region in self:
            priority_indicator = ' 🔶' if region.mining_area else ''
            name = f"[{region.code}] {region.name}{priority_indicator}"
            result.append((region.id, name))
        return result
