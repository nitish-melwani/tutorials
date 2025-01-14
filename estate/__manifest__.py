# -*- coding: utf-8 -*-
{
    'name': "Estate",

    'application': True,
    'depends': ['base'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_user_views.xml',
        'views/estate_menus.xml',
    ],
}
