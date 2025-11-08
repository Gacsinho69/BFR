# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """
    Extensión del modelo res.partner para BAUFER.

    Agrega campos específicos para:
    - Clasificación de clientes (tipo, sector)
    - Información de flota y equipos
    - Scoring y métricas comerciales
    - SLA y calidad de servicio
    - Términos comerciales y crédito
    """
    _inherit = 'res.partner'

    # =============================
    # DATOS COMERCIALES
    # =============================

    customer_type = fields.Selection(
        selection=[
            ('rental', 'Arriendo Maquinaria'),
            ('transport', 'Transporte'),
            ('construction', 'Construcción'),
            ('mining', 'Minería'),
            ('other', 'Otro')
        ],
        string='Tipo Cliente',
        help='Clasificación del cliente según sector de actividad'
    )

    fleet_size = fields.Integer(
        string='Tamaño Flota',
        help='Cantidad aproximada de equipos en la flota del cliente'
    )

    main_brands = fields.Many2many(
        'product.brand',
        'partner_brand_rel',
        'partner_id',
        'brand_id',
        string='Marcas Principales',
        help='Marcas de maquinaria que opera el cliente (Caterpillar, Komatsu, etc.)'
    )

    equipment_types = fields.Many2many(
        'product.category',
        'partner_category_rel',
        'partner_id',
        'category_id',
        string='Tipos Equipos',
        help='Categorías de equipos que opera (Excavadoras, Cargadores, etc.)'
    )

    region_operations = fields.Many2many(
        'baufer.region',
        'partner_region_rel',
        'partner_id',
        'region_id',
        string='Regiones Operación',
        help='Regiones de Chile donde el cliente tiene operaciones'
    )

    credit_days = fields.Integer(
        string='Días Crédito',
        default=30,
        help='Días de crédito otorgados al cliente'
    )

    payment_terms = fields.Selection(
        selection=[
            ('cash', 'Contado'),
            ('credit_15', 'Crédito 15 días'),
            ('credit_30', 'Crédito 30 días'),
            ('credit_60', 'Crédito 60 días')
        ],
        string='Términos Pago',
        default='credit_30',
        help='Términos de pago acordados con el cliente'
    )

    # =============================
    # SCORING Y MÉTRICAS
    # =============================

    lifetime_value = fields.Monetary(
        string='Valor Lifetime',
        currency_field='currency_id',
        compute='_compute_lifetime_value',
        store=True,
        help='Valor total de compras históricas del cliente'
    )

    average_ticket = fields.Monetary(
        string='Ticket Promedio',
        currency_field='currency_id',
        compute='_compute_average_ticket',
        store=True,
        help='Valor promedio de órdenes de venta'
    )

    purchase_frequency = fields.Float(
        string='Frecuencia Compra Mensual',
        compute='_compute_purchase_frequency',
        store=True,
        help='Número promedio de compras por mes'
    )

    last_purchase_date = fields.Date(
        string='Última Compra',
        compute='_compute_last_purchase_date',
        store=True,
        help='Fecha de la última orden de venta confirmada'
    )

    risk_level = fields.Selection(
        selection=[
            ('low', 'Bajo'),
            ('medium', 'Medio'),
            ('high', 'Alto')
        ],
        string='Nivel Riesgo',
        default='low',
        help='Nivel de riesgo crediticio del cliente'
    )

    # =============================
    # SLA Y ATENCIÓN
    # =============================

    sla_15min_compliance = fields.Float(
        string='Cumplimiento SLA 15min (%)',
        compute='_compute_sla_compliance',
        store=True,
        help='Porcentaje de cumplimiento del SLA de 15 minutos para primer contacto'
    )

    average_response_time = fields.Float(
        string='Tiempo Respuesta Promedio (min)',
        compute='_compute_average_response_time',
        store=True,
        help='Tiempo promedio de primer contacto en minutos'
    )

    nps_score = fields.Integer(
        string='Net Promoter Score',
        help='Puntuación NPS del cliente (0-10)'
    )

    # =============================
    # CAMPOS INFORMATIVOS
    # =============================

    is_mining_sector = fields.Boolean(
        string='Sector Minero',
        compute='_compute_is_mining_sector',
        store=True,
        help='Indica si el cliente pertenece al sector minero'
    )

    total_orders = fields.Integer(
        string='Total Órdenes',
        compute='_compute_total_orders',
        store=True,
        help='Número total de órdenes de venta'
    )

    # =============================
    # COMPUTED FIELDS
    # =============================

    @api.depends('customer_type', 'region_operations')
    def _compute_is_mining_sector(self):
        """Determina si el cliente es del sector minero."""
        for partner in self:
            is_mining = partner.customer_type == 'mining'
            has_mining_regions = any(region.mining_area for region in partner.region_operations)
            partner.is_mining_sector = is_mining or has_mining_regions

    @api.depends('sale_order_ids.amount_total', 'sale_order_ids.state')
    def _compute_lifetime_value(self):
        """Calcula el valor total de compras del cliente."""
        for partner in self:
            confirmed_orders = partner.sale_order_ids.filtered(
                lambda o: o.state in ('sale', 'done')
            )
            partner.lifetime_value = sum(confirmed_orders.mapped('amount_total'))

    @api.depends('sale_order_ids.amount_total', 'sale_order_ids.state')
    def _compute_average_ticket(self):
        """Calcula el ticket promedio de compras."""
        for partner in self:
            confirmed_orders = partner.sale_order_ids.filtered(
                lambda o: o.state in ('sale', 'done')
            )
            order_count = len(confirmed_orders)
            if order_count > 0:
                partner.average_ticket = sum(confirmed_orders.mapped('amount_total')) / order_count
            else:
                partner.average_ticket = 0.0

    @api.depends('sale_order_ids.date_order', 'sale_order_ids.state')
    def _compute_purchase_frequency(self):
        """Calcula la frecuencia de compra mensual."""
        for partner in self:
            confirmed_orders = partner.sale_order_ids.filtered(
                lambda o: o.state in ('sale', 'done')
            )
            if confirmed_orders:
                first_order = min(confirmed_orders.mapped('date_order'))
                last_order = max(confirmed_orders.mapped('date_order'))
                months_diff = (last_order.year - first_order.year) * 12 + (last_order.month - first_order.month)
                if months_diff > 0:
                    partner.purchase_frequency = len(confirmed_orders) / months_diff
                else:
                    partner.purchase_frequency = len(confirmed_orders)
            else:
                partner.purchase_frequency = 0.0

    @api.depends('sale_order_ids.date_order', 'sale_order_ids.state')
    def _compute_last_purchase_date(self):
        """Obtiene la fecha de la última compra."""
        for partner in self:
            confirmed_orders = partner.sale_order_ids.filtered(
                lambda o: o.state in ('sale', 'done')
            )
            if confirmed_orders:
                partner.last_purchase_date = max(confirmed_orders.mapped('date_order'))
            else:
                partner.last_purchase_date = False

    @api.depends('sale_order_ids')
    def _compute_total_orders(self):
        """Calcula el total de órdenes de venta."""
        for partner in self:
            partner.total_orders = len(partner.sale_order_ids.filtered(
                lambda o: o.state in ('sale', 'done')
            ))

    def _compute_sla_compliance(self):
        """Calcula el cumplimiento del SLA de 15 minutos."""
        for partner in self:
            # Este cálculo se completará cuando exista el módulo baufer_crm
            # Por ahora, establecemos un valor por defecto
            partner.sla_15min_compliance = 100.0

    def _compute_average_response_time(self):
        """Calcula el tiempo promedio de respuesta."""
        for partner in self:
            # Este cálculo se completará cuando exista el módulo baufer_crm
            # Por ahora, establecemos un valor por defecto
            partner.average_response_time = 10.0

    # =============================
    # CONSTRAINTS
    # =============================

    @api.constrains('credit_days')
    def _check_credit_days(self):
        """Valida que los días de crédito sean positivos."""
        for partner in self:
            if partner.credit_days and partner.credit_days < 0:
                raise ValidationError(_('Los días de crédito deben ser un valor positivo.'))

    @api.constrains('nps_score')
    def _check_nps_score(self):
        """Valida que el NPS esté entre 0 y 10."""
        for partner in self:
            if partner.nps_score and (partner.nps_score < 0 or partner.nps_score > 10):
                raise ValidationError(_('El NPS Score debe estar entre 0 y 10.'))

    @api.constrains('fleet_size')
    def _check_fleet_size(self):
        """Valida que el tamaño de flota sea positivo."""
        for partner in self:
            if partner.fleet_size and partner.fleet_size < 0:
                raise ValidationError(_('El tamaño de flota debe ser un valor positivo.'))

    # =============================
    # MÉTODOS DE ACCIÓN
    # =============================

    def action_view_orders(self):
        """Abre vista de órdenes de venta del cliente."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Órdenes de Venta'),
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id}
        }

    def action_view_opportunities(self):
        """Abre vista de oportunidades/leads del cliente."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Oportunidades'),
            'res_model': 'crm.lead',
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id}
        }
