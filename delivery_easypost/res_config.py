
from openerp.osv import fields, osv 

class easypost_config_settings(osv.osv_memory):
    _name = 'easypost.config.settings'
    _inherit = 'res.config.settings'

    _columns = {
        'default_ep_apikey': fields.char('Easypost API Key', size=32, default_model='easypost.config.settingsl'),
        'default_ep_company': fields.char('From Address - Company', size=64, default_model='easypost.config.settingsl'),
        'default_ep_phone': fields.char('From Address - Phone Number', size=64, default_model='easypost.config.settingsl'),
        'default_ep_street1': fields.char('From Address - Street Line 1', size=64, default_model='easypost.config.settingsl'),
        'default_ep_street2': fields.char('From Address - Street Line 2', size=64, default_model='easypost.config.settingsl'),
        'default_ep_city': fields.char('From Address - City', size=64, default_model='easypost.config.settingsl'),
        'default_ep_state': fields.char('From Address - State (2 letter code)', size=64, default_model='easypost.config.settingsl'),
        'default_ep_zip': fields.char('From Address - Zip / Postal code', size=64, default_model='easypost.config.settingsl'),
        'default_ep_country': fields.char('From Address - Country', size=64, default_model='easypost.config.settingsl'),
        'default_ep_email': fields.char('From Address - eMail', size=64, default_model='easypost.config.settingsl'),
    }
    _defaults = {
        'default_ep_apikey': "apikey",
        'default_ep_company': 'company',
        'default_ep_phone': '1234567890',
        'default_ep_street1': '123 test street',
        'default_ep_street2': 'Unit 1',
        'default_ep_city': 'Cityname',
        'default_ep_state': 'ON',
        'default_ep_zip': 'A2A4A4',
        'default_ep_country': 'CA',
        'default_ep_email': 'someemail@site.com',
    }