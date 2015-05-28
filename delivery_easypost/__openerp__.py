{
    'name': 'EasyPost Delivery Costs',
    'version': '20140313.01',
    'author': 'Will Xyen',
    'category': 'Delivery',
    'depends': ['product','delivery','sale_stock', 'website_sale', 'website_sale_delivery', 'product_dimensions'],
    'init_xml': [],
    'data': [
        "delivery_view.xml",
        "checkout_view.xml",
        "carrier_data.xml",
        "res_config.xml",
    ],
    'demo_xml': [],
    'test': [],
    'qweb' : [
        #"static/src/xml/base.xml",
    ],
    'installable': True,
	'auto_install' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
