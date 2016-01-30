﻿# -*- encoding: utf-8 -*-
# (C) Eino Mäkitalo, Aviapartio ry.  MIT License or LGPL if you like.
# Based on voluntary work.
{
    'name': 'Finnish template for local scout groups',
    'version': '9.0.0.1.0',
    'author': 'Aviapartio ry. / Eino Mäkitalo',
    'category': 'Localization/Account Charts',
    'description': """
Example chart of account template for local scout group
=======================================================
Local Scout groups are  non-profit organizations and mostly
without tax issues. This template is planned to use with Aviapartio ry.
See more information about Finnish scouting and account issues from 
http://purkki.partio.fi

    """,
    'depends': [
        'account', 
        'base_iban', 
    ],
    'data': [
        'account_chart.xml', 
        'account_chart_template.yml'
    ],
    'test': [],
    'demo': [],
    'auto_install': False,
    'installable': True,
}
