# -*- coding: utf-8 -*-
import os.path
import time
import math


from openerp.osv import fields, osv
import logging
logging.getLogger("requests").setLevel(logging.WARNING)
_logger = logging.getLogger(__name__)

class delivery_grid(osv.osv):
    _inherit = "delivery.grid"

    def get_price_from_picking(self, cr, uid, id, total, weight, volume, quantity, context=None):
        grid = self.browse(cr, uid, id, context=context)
        price = 0.0
        ok = False

        order_id = context.get('order_id',False)

        volume = 0

        if order_id:
            order = self.pool.get('sale.order').browse(cr, uid, order_id, context=context)
            contact = self.pool.get('res.partner').browse(cr, uid, order.partner_shipping_id.id, context=context)
            
            c_val = contact.country_id.code
            s_val = contact.state_id.code

            for line in order.order_line:
                if line.product_id:
                    volume += line.product_id.length*line.product_id.height*line.product_id.width*line.product_uom_qty
        else:
            _logger.info(context)
            raise osv.except_osv("", "Unable to fetch delivery method! No order ID!!!!")

        if volume <= 0:
            volume = 4000
        if weight <= 0:
            weight = 0.45
        weight += 0.300
        # for packing weight

        price_dict = {'price': total, 'volume':volume, 'weight': weight, 'wv':volume*weight, 'quantity': quantity}
        
        for line in grid.line_ids:
            test = eval(line.type+line.operator+str(line.max_value), price_dict)
            if test:
                if line.price_type=='variable':
                    price = line.list_price * price_dict[line.variable_factor]
                    ok = True
                    break
                elif line.price_type=='easypost':
                    config = self.pool.get('easypost.config.settings').default_get(
                        cr, 
                        uid, 
                        [
                            'default_ep_apikey',
                            'default_ep_company',
                            'default_ep_phone',
                            'default_ep_street1',
                            'default_ep_street2',
                            'default_ep_city',
                            'default_ep_state',
                            'default_ep_zip',
                            'default_ep_country',
                            'default_ep_email',
                        ],
                        context
                    )

                    if 'Intl' in line.d_type_keyword or 'International' in line.d_type_keyword:
                        if config['default_ep_country']==c_val:
                            raise osv.except_osv("", "Not using since not international.")
                    elif 'USA' in line.d_type_keyword:
                        if c_val != 'US':
                            raise osv.except_osv("", "Not using since not to the US.")

                    divider = 1
                    if (weight * 35.274) > 300:
                        divider = math.ceil(weight * 35.274 / 300)
                        weight /= divider
                    if not os.path.exists("/tmp/easypost_cache/"):
                        try:
                            os.makedirs("/tmp/easypost_cache/")
                        except OSError as exception:
                            if exception.errno != errno.EEXIST:
                                raise
                    pickleName = "/tmp/easypost_cache/"+str(config["default_ep_zip"])+"Z"+str(weight) + "Z" + str(volume) + c_val + "Z" + s_val + "Z" + contact.city + "Z" + contact.zip + "Z" + time.strftime("%d-%m-%Y") + ".pickle"
                    import pickle
                    if os.path.isfile(pickleName):
                        price_list = pickle.load(open(pickleName, 'rb'))
                        if price_list:
                            '''_logger.info('Using Cached Prices')'''
                            '''_logger.info(price_list)'''
                        else:
                            raise osv.except_osv("Cached Price is NULL: ", pickleName)
                    else:
                        import easypost
                        

                        '''
                        config = self.pool.get('easypost.config.settings').browse(cr, uid, id, context=context)
                        '''
                        _logger.info('config load')
                        easypost.api_key = config['default_ep_apikey']
                        _logger.info('get config')

                        if contact.street != contact.street2 and contact.street2 != "" and contact.street2:
                            to_address = easypost.Address.create(
                                name = contact.name,
                                street1 = contact.street,
                                street2 = contact.street2,
                                city = contact.city,
                                zip = contact.zip,
                                country = c_val,
                                state = s_val,
                            )
                        else:
                            to_address = easypost.Address.create(
                                name = contact.name,
                                street1 = contact.street,
                                city = contact.city,
                                zip = contact.zip,
                                country = c_val,
                                state = s_val,
                            )
                        try:
                            price_list = get_all_prices(config, weight, volume, to_address)
                            pickle.dump(price_list, open(pickleName, 'wb'), -1)
                        except easypost.Error as e:
                            pickle.dump(None, open(pickleName, 'wb'), -1)
                            if e.param != None:
                                raise osv.except_osv("Easy Post Specifically an invalid param: ", e.param)
                            else:
                                raise osv.except_osv("Easy Post: ", e.message)

                    for ship_method in price_list['rates']:
                        if ship_method['carrier']==line.d_carrier_keyword:
                            if ship_method['service']==line.d_type_keyword:
                                '''_logger.info(ship_method['service'] + ship_method['rate'])'''
                                price = float(ship_method['rate'])*divider + line.list_price
                                ok = True
                                break
                else:
                    price = line.list_price
                    ok = True
                    break
        if not ok:
            raise osv.except_osv("", "Selected product in the delivery method doesn't fulfill any of the delivery grid(s) criteria.")

        return price
delivery_grid()

def get_all_prices(config, weight, volume, _to_address):
    import easypost
    import pprint
    easypost.api_key = config['default_ep_apikey']

    _from_address = easypost.Address.create(
        name = config['default_ep_apikey'],
        company = config['default_ep_company'],
        phone = config['default_ep_phone'],
        street1 = config['default_ep_street1'],
        street2 = config['default_ep_street2'],
        city = config['default_ep_city'],
        state = config['default_ep_state'],
        zip = config['default_ep_zip'],
        country = config['default_ep_country'],
        email = config['default_ep_email'],
    )
    if volume < 0.001:
        volume = 0.001
    _parcel = easypost.Parcel.create(
        length = volume ** (1 / 3.0)*0.393701, 
        width = volume ** (1 / 3.0)*0.393701,
        height = volume ** (1 / 3.0)*0.393701, #cm to inch
        weight = weight * 35.274 #kg to oz
    )

    shipment = easypost.Shipment.create(
        to_address = _to_address,
        from_address = _from_address,
        buyer_address = _from_address,
        parcel = _parcel,
        customs_info = easypost.CustomsInfo.create(
            contents_type = 'merchandise',
            restriction_type = 'none',
            customs_items = [{
                'description': 'Toys',
                'quantity': 1,
                'value': 10,
                'weight': weight,
                'origin_country': 'CA'
            }]
        ),
        options = {'currency':"CAD"}
    )
    _logger.info(_parcel)
    return shipment.get_rates()

class delivery_grid_line(osv.osv):
    _inherit = "delivery.grid.line"
    _name = 'delivery.grid.line'
    _columns = {
        'd_carrier_keyword' : fields.char('Shipping Carrier Keyword', size=32),
        'd_type_keyword' : fields.char('Shipping Type Keyword', size=64),
        'price_type': fields.selection([('fixed','Fixed'),('variable','Variable'),('easypost','Easy Post')], 'Price Type', required=True),
    }

delivery_grid_line()