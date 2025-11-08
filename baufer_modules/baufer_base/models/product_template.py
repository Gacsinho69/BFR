# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    """
    Extensión del modelo product.template para BAUFER.

    Agrega campos específicos para repuestos de maquinaria pesada:
    - Números de parte (OEM y fabricante)
    - Marca y tipo de motor
    - Información de importación
    - Stock crítico y lead times
    - Compatibilidad con equipos
    """
    _inherit = 'product.template'

    # =============================
    # IDENTIFICACIÓN DE PARTE
    # =============================

    part_number = fields.Char(
        string='Número Parte',
        required=False,  # No requerido para todos los productos, solo repuestos
        index=True,
        help='Número de parte del fabricante'
    )

    oem_number = fields.Char(
        string='Número OEM',
        index=True,
        help='Número de parte original del fabricante del equipo (OEM)'
    )

    brand_id = fields.Many2one(
        'product.brand',
        string='Marca',
        index=True,
        help='Marca del repuesto (Caterpillar, Komatsu, etc.)'
    )

    # =============================
    # TIPO Y COMPATIBILIDAD
    # =============================

    engine_type = fields.Selection(
        selection=[
            ('diesel', 'Diesel'),
            ('gasoline', 'Gasolina'),
            ('gas', 'Gas'),
            ('electric', 'Eléctrico'),
            ('hybrid', 'Híbrido'),
            ('na', 'No Aplica')
        ],
        string='Tipo Motor',
        default='na',
        help='Tipo de motor al que aplica el repuesto'
    )

    equipment_model = fields.Char(
        string='Modelo Equipo Compatible',
        help='Modelo(s) de equipo compatible con este repuesto (ej: 320D, PC200, etc.)'
    )

    compatible_brands = fields.Many2many(
        'product.brand',
        'product_compatible_brand_rel',
        'product_id',
        'brand_id',
        string='Marcas Compatibles',
        help='Marcas de equipos con las que es compatible este repuesto'
    )

    # =============================
    # CRITICIDAD Y STOCK
    # =============================

    critical_part = fields.Boolean(
        string='Parte Crítica',
        default=False,
        help='Indica si es una parte crítica que requiere stock mínimo garantizado'
    )

    minimum_stock = fields.Float(
        string='Stock Mínimo',
        default=0.0,
        help='Cantidad mínima que debe mantenerse en stock'
    )

    current_stock = fields.Float(
        string='Stock Actual',
        compute='_compute_current_stock',
        store=False,
        help='Stock disponible actual'
    )

    stock_status = fields.Selection(
        selection=[
            ('in_stock', 'En Stock'),
            ('low_stock', 'Stock Bajo'),
            ('out_of_stock', 'Sin Stock'),
            ('to_order', 'Por Pedir')
        ],
        string='Estado Stock',
        compute='_compute_stock_status',
        store=True,
        help='Estado actual del stock'
    )

    # =============================
    # IMPORTACIÓN Y PROVEEDORES
    # =============================

    lead_time_days = fields.Integer(
        string='Lead Time Importación (días)',
        default=30,
        help='Días estimados desde orden de compra hasta recepción'
    )

    supplier_id = fields.Many2one(
        'res.partner',
        string='Proveedor Principal',
        domain="[('supplier_rank', '>', 0)]",
        help='Proveedor habitual para este producto'
    )

    last_import_date = fields.Date(
        string='Última Importación',
        help='Fecha de la última recepción de importación'
    )

    import_frequency = fields.Integer(
        string='Frecuencia Importación (días)',
        default=90,
        help='Frecuencia promedio de importación en días'
    )

    next_import_date = fields.Date(
        string='Próxima Importación',
        compute='_compute_next_import_date',
        store=True,
        help='Fecha estimada de próxima importación'
    )

    # =============================
    # INFORMACIÓN COMERCIAL
    # =============================

    sales_count = fields.Integer(
        string='Cantidad Vendida',
        compute='_compute_sales_count',
        store=True,
        help='Cantidad total vendida de este producto'
    )

    last_sale_date = fields.Date(
        string='Última Venta',
        compute='_compute_last_sale_date',
        store=True,
        help='Fecha de la última venta de este producto'
    )

    rotation_category = fields.Selection(
        selection=[
            ('high', 'Alta Rotación'),
            ('medium', 'Rotación Media'),
            ('low', 'Baja Rotación'),
            ('obsolete', 'Obsoleto')
        ],
        string='Categoría Rotación',
        compute='_compute_rotation_category',
        store=True,
        help='Categoría de rotación basada en ventas'
    )

    # =============================
    # COMPUTED FIELDS
    # =============================

    @api.depends('product_variant_ids.qty_available')
    def _compute_current_stock(self):
        """Calcula el stock actual disponible."""
        for product in self:
            product.current_stock = sum(product.product_variant_ids.mapped('qty_available'))

    @api.depends('current_stock', 'minimum_stock', 'critical_part')
    def _compute_stock_status(self):
        """Determina el estado del stock."""
        for product in self:
            if product.current_stock <= 0:
                product.stock_status = 'out_of_stock'
            elif product.critical_part and product.current_stock <= product.minimum_stock:
                product.stock_status = 'low_stock'
            elif product.current_stock <= product.minimum_stock:
                product.stock_status = 'to_order'
            else:
                product.stock_status = 'in_stock'

    @api.depends('last_import_date', 'import_frequency')
    def _compute_next_import_date(self):
        """Calcula la fecha estimada de próxima importación."""
        for product in self:
            if product.last_import_date and product.import_frequency:
                from datetime import timedelta
                product.next_import_date = product.last_import_date + timedelta(days=product.import_frequency)
            else:
                product.next_import_date = False

    @api.depends('product_variant_ids.sales_count')
    def _compute_sales_count(self):
        """Calcula la cantidad total vendida."""
        for product in self:
            # Este cálculo se puede mejorar cuando tengamos el módulo sale
            product.sales_count = sum(product.product_variant_ids.mapped('sales_count'))

    def _compute_last_sale_date(self):
        """Obtiene la fecha de la última venta."""
        for product in self:
            # Este cálculo se completará cuando se integre con sale.order.line
            product.last_sale_date = False

    @api.depends('sales_count')
    def _compute_rotation_category(self):
        """Clasifica el producto según su rotación."""
        for product in self:
            if product.sales_count >= 50:
                product.rotation_category = 'high'
            elif product.sales_count >= 20:
                product.rotation_category = 'medium'
            elif product.sales_count >= 5:
                product.rotation_category = 'low'
            else:
                product.rotation_category = 'obsolete'

    # =============================
    # CONSTRAINTS
    # =============================

    @api.constrains('part_number', 'brand_id')
    def _check_part_number_brand(self):
        """Valida unicidad de part_number por marca."""
        for product in self:
            if product.part_number and product.brand_id:
                duplicates = self.search([
                    ('id', '!=', product.id),
                    ('part_number', '=', product.part_number),
                    ('brand_id', '=', product.brand_id.id)
                ])
                if duplicates:
                    raise ValidationError(
                        _('Ya existe un producto con el número de parte "%s" para la marca "%s".')
                        % (product.part_number, product.brand_id.name)
                    )

    @api.constrains('minimum_stock')
    def _check_minimum_stock(self):
        """Valida que el stock mínimo sea positivo."""
        for product in self:
            if product.minimum_stock < 0:
                raise ValidationError(_('El stock mínimo no puede ser negativo.'))

    @api.constrains('lead_time_days')
    def _check_lead_time(self):
        """Valida que el lead time sea positivo."""
        for product in self:
            if product.lead_time_days < 0:
                raise ValidationError(_('El lead time no puede ser negativo.'))

    @api.constrains('import_frequency')
    def _check_import_frequency(self):
        """Valida que la frecuencia de importación sea positiva."""
        for product in self:
            if product.import_frequency < 0:
                raise ValidationError(_('La frecuencia de importación no puede ser negativa.'))

    # =============================
    # MÉTODOS DE ACCIÓN
    # =============================

    def action_view_stock_moves(self):
        """Abre vista de movimientos de stock del producto."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Movimientos de Stock'),
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [('product_id', 'in', self.product_variant_ids.ids)],
            'context': {'default_product_id': self.product_variant_ids[:1].id}
        }

    def action_request_import(self):
        """Crea solicitud de importación para el producto."""
        self.ensure_one()
        # Esta acción se completará cuando exista el módulo de compras/importación
        return {
            'type': 'ir.actions.act_window',
            'name': _('Solicitar Importación'),
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'context': {
                'default_partner_id': self.supplier_id.id if self.supplier_id else False,
            }
        }

    def name_get(self):
        """Formato de visualización con número de parte."""
        result = []
        for product in self:
            name = product.name
            if product.part_number:
                name = f"[{product.part_number}] {name}"
            if product.brand_id:
                name = f"{name} - {product.brand_id.code}"
            result.append((product.id, name))
        return result
