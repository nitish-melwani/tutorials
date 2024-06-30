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
        'views/estate_sales_person_views.xml',
        'views/estate_menus.xml',
    ],
}
