
from openerp import SUPERUSER_ID
from openerp import http, addons
from openerp.http import request
from openerp.addons.website.models.website import slug

import logging
_logger = logging.getLogger(__name__)

class website_sale_ext(addons.website_sale.controllers.main.website_sale):
    mandatory_billing_fields = ["street", "state_id", "zip", "name", "phone", "email", "street", "city", "country_id"]
    optional_billing_fields = ["vat", "vat_subjected", "street2"]
    mandatory_shipping_fields = ["name", "phone", "street", "city", "country_id", "state_id", "zip"]
    optional_shipping_fields = ["street2"]
    
website_sale_ext()