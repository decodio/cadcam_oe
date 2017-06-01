



class product_product(osv.osv):
    _name = "product.product"
    _inherit = "product.product"

    _columns = {
        'total_id': fields.integer('Close', help="Alternative identificator from TOTAL"),
    }



