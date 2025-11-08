# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductBrand(models.Model):
    """
    Modelo para gestión de marcas de maquinaria pesada.

    Marcas principales: Caterpillar, Komatsu, John Deere, Volvo, JCB, Case,
    Hyundai, Doosan, Hyster, Yale.
    """
    _name = 'product.brand'
    _description = 'Marca de Producto'
    _order = 'name'

    name = fields.Char(
        string='Nombre Marca',
        required=True,
        index=True,
        help='Nombre de la marca (ej: Caterpillar, Komatsu)'
    )

    code = fields.Char(
        string='Código',
        required=True,
        index=True,
        help='Código corto de la marca (ej: CAT, KOM)'
    )

    description = fields.Text(
        string='Descripción',
        help='Descripción de la marca y sus características'
    )

    logo = fields.Binary(
        string='Logo',
        help='Logo de la marca'
    )

    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Si está inactivo, la marca no se mostrará en selecciones'
    )

    product_count = fields.Integer(
        string='Cantidad Productos',
        compute='_compute_product_count',
        store=False,
        help='Número de productos de esta marca'
    )

    partner_count = fields.Integer(
        string='Cantidad Clientes',
        compute='_compute_partner_count',
        store=False,
        help='Número de clientes que trabajan con esta marca'
    )

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'El código de marca debe ser único!'),
        ('name_uniq', 'unique(name)', 'El nombre de marca debe ser único!'),
    ]

    @api.depends('name')
    def _compute_product_count(self):
        """Calcula la cantidad de productos por marca."""
        for brand in self:
            brand.product_count = self.env['product.template'].search_count([
                ('brand_id', '=', brand.id)
            ])

    @api.depends('name')
    def _compute_partner_count(self):
        """Calcula la cantidad de clientes asociados a esta marca."""
        for brand in self:
            brand.partner_count = self.env['res.partner'].search_count([
                ('main_brands', 'in', brand.id)
            ])

    @api.constrains('code')
    def _check_code_uppercase(self):
        """Valida que el código esté en mayúsculas."""
        for brand in self:
            if brand.code and brand.code != brand.code.upper():
                raise ValidationError('El código de marca debe estar en mayúsculas.')

    def name_get(self):
        """Formato de visualización: [CODE] Name."""
        result = []
        for brand in self:
            name = f"[{brand.code}] {brand.name}"
            result.append((brand.id, name))
        return result
