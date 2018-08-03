#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2016-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from __future__ import print_function

import images

# import argparse
# import getpass

# import openerplib
# import erppeek
# import xmlrpclib

from odoo_client.cli import *
from odoo_client.install import *

upgrade = False
CompanyName = 'CLVhealth-JCAFB'
Slogan = 'Uma vez Jornadeiro, sempre Jornadeiro'
Company_image = images.Company_image
website = 'https://github.com/CLVsol'
admin_user_email = 'admin@clvsol.com'
Administrator_image = images.Administrator_image
Demo_User_image = images.Demo_User_image
DataAdministrator_image = images.DataAdministrator_image
demo_user_name = 'Demo User'
demo_user = 'demo'
demo_user_pw = 'demo'
demo_user_email = 'demo.user@clvsol.com'
data_admin_user_name = 'Data Administrator'
data_admin_user = 'data.admin'
data_admin_user_pw = 'data.admin'
data_admin_user_email = 'data.admin@clvsol.com'

# lang = 'en_US'
lang = 'pt_BR'  # use Translation: Portuguese(BR)/Portugues(BR)
tz = 'America/Sao_Paulo'

hostname = 'localhost'
server = 'http://localhost:8069'
admin = 'admin'
admin_user = 'admin'

admin_pw = 'admin'
admin_user_pw = 'admin'
data_admin_user_pw = 'data.admin'
dbname = 'clvhealth_jcafb'
demo_data = False
modules_to_upgrade = []

sock_common_url = 'http://localhost:8069/xmlrpc/common'
sock_str = 'http://localhost:8069/xmlrpc/object'


def get_arguments():

    global upgrade
    global admin_pw
    global admin_user_pw
    global data_admin_user_pw
    global dbname
    global demo_data
    global modules_to_upgrade

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--upgrade_all', action='store_true', help='Update all the modules')
    parser.add_argument('--admin_pw', action="store", dest="admin_pw")
    parser.add_argument('--admin_user_pw', action="store", dest="admin_user_pw")
    parser.add_argument('--data_admin_user_pw', action="store", dest="data_admin_user_pw")
    parser.add_argument('--dbname', action="store", dest="dbname")
    parser.add_argument('-d', '--demo_data', action='store_true', help='Install demo data')
    parser.add_argument('-m', '--modules', nargs='+', help='Modules to upgrade', required=False)

    args = parser.parse_args()

    print('\n%s%s\n' % ('--> ', args))

    upgrade = args.upgrade_all

    if args.admin_pw is not None:
        admin_pw = args.admin_pw
    elif admin_pw == '*':
        admin_pw = getpass.getpass('admin_pw: ')

    if args.admin_user_pw is not None:
        admin_user_pw = args.admin_user_pw
    elif admin_user_pw == '*':
        admin_user_pw = getpass.getpass('admin_user_pw: ')

    if args.data_admin_user_pw is not None:
        data_admin_user_pw = args.data_admin_user_pw
    elif data_admin_user_pw == '*':
        data_admin_user_pw = getpass.getpass('data_admin_user_pw: ')

    if args.dbname is not None:
        dbname = args.dbname
    elif dbname == '*':
        dbname = raw_input('dbname: ')

    demo_data = args.demo_data

    if args.modules is not None:
        modules_to_upgrade = args.modules
    else:
        modules_to_upgrade = []


def MyCompany():

    print('Configuring My Company...')

    sock_common = xmlrpclib.ServerProxy(sock_common_url)
    uid = sock_common.login(dbname, admin_user, admin_user_pw)
    sock = xmlrpclib.ServerProxy(sock_str)

    args = [('name', '=', 'My Company'), ]
    partner_id = sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'search', args)
    values = {
        'name': CompanyName,
        'email': '',
        'website': website,
        'tz': tz,
        'lang': lang,
        'image': Company_image,
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'write', partner_id, values)

    args = [('name', '=', 'My Company'), ]
    company_id = sock.execute(dbname, uid, admin_user_pw, 'res.company', 'search', args)
    values = {
        'name': CompanyName,
        'email': '',
        'website': website,
        'rml_header1': Slogan,
        'logo': Company_image,
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.company', 'write', company_id, values)

    print('Done.')


def Administrator():

    print('Configuring user "Administrator"...')

    sock_common = xmlrpclib.ServerProxy(sock_common_url)
    uid = sock_common.login(dbname, admin_user, admin_user_pw)
    sock = xmlrpclib.ServerProxy(sock_str)

    args = [('name', '=', 'Administrator'), ]
    user_id = sock.execute(dbname, uid, admin_user_pw, 'res.users', 'search', args)
    values = {
        'lang': lang,
        'tz': tz,
        'email': admin_user_email,
        'image': Administrator_image,
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.users', 'write', user_id, values)

    values = {
        'groups_id': [(6, 0, [
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Access Rights')])[0],
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Settings')])[0],
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Employee')])[0],
            # sock.execute(
            #     dbname, uid, admin_user_pw,
            #     'res.groups', 'search', [('name', '=', 'Multi Companies')])[0],
            # sock.execute(
            #     dbname, uid, admin_user_pw,
            #     'res.groups', 'search', [('name', '=', 'Multi Currencies')])[0],
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Technical Features')])[0],
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Contact Creation')])[0],
        ])],
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.users', 'write', user_id, values)

    print('Done.')


def Demo_User():

    print('Configuring user "Demo"...')

    sock_common = xmlrpclib.ServerProxy(sock_common_url)
    uid = sock_common.login(dbname, admin_user, admin_user_pw)
    sock = xmlrpclib.ServerProxy(sock_str)

    args = [('name', '=', CompanyName), ]
    parent_id = sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'search', args)
    args = [('name', '=', CompanyName), ]
    company_id = sock.execute(dbname, uid, admin_user_pw, 'res.company', 'search', args)

    values = {
        'name': demo_user_name,
        'customer': False,
        'employee': False,
        'is_company': False,
        'email': demo_user_email,
        'website': '',
        'parent_id': parent_id[0],
        'company_id': company_id[0],
        'tz': tz,
        'lang': lang
    }
    partner_id = sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'create', values)

    values = {
        'name': demo_user_name,
        'partner_id': partner_id,
        'company_id': company_id[0],
        'login': demo_user,
        'password': demo_user_pw,
        'image': Demo_User_image,
        'groups_id': [(6, 0, [])],
    }
    user_id = sock.execute(dbname, uid, admin_user_pw, 'res.users', 'create', values)

    values = {
        'groups_id': [(6, 0, [
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Employee')])[0],
        ])],
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.users', 'write', user_id, values)

    print('Done.')


def Data_Administrator_User():

    print('Configuring user "Data Administrator"...')

    sock_common = xmlrpclib.ServerProxy(sock_common_url)
    uid = sock_common.login(dbname, admin_user, admin_user_pw)
    sock = xmlrpclib.ServerProxy(sock_str)

    args = [('name', '=', CompanyName), ]
    parent_id = sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'search', args)
    args = [('name', '=', CompanyName), ]
    company_id = sock.execute(dbname, uid, admin_user_pw, 'res.company', 'search', args)

    values = {
        'name': data_admin_user_name,
        'customer': False,
        'employee': False,
        'is_company': False,
        'email': data_admin_user_email,
        'website': '',
        'parent_id': parent_id[0],
        'company_id': company_id[0],
        'tz': tz,
        'lang': lang
    }
    partner_id = sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'create', values)

    values = {
        'name': data_admin_user_name,
        'partner_id': partner_id,
        'company_id': company_id[0],
        'login': data_admin_user,
        'password': data_admin_user_pw,
        'image': DataAdministrator_image,
        'groups_id': [(6, 0, [])],
    }
    user_id = sock.execute(dbname, uid, admin_user_pw, 'res.users', 'create', values)

    values = {
        'groups_id': [(6, 0, [
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Employee')])[0],
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Contact Creation')])[0],
        ])],
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.users', 'write', user_id, values)

    print('Done.')


def user_groups_set(user_name, group_name_list):

    print('Executing user_groups_set...')

    sock_common = xmlrpclib.ServerProxy(sock_common_url)
    uid = sock_common.login(dbname, admin_user, admin_user_pw)
    sock = xmlrpclib.ServerProxy(sock_str)

    args = [('name', '=', user_name), ]
    user_id = sock.execute(dbname, uid, admin_user_pw, 'res.users', 'search', args)

    for group_name in group_name_list:
        values = {
            'groups_id': [(
                4, sock.execute(dbname, uid, admin_user_pw,
                                'res.groups', 'search', [('name', '=', group_name)]
                                )[0]
            )],
        }
        sock.execute(dbname, uid, admin_user_pw, 'res.users', 'write', user_id, values)

    print('Done.')


def install_upgrade_module(module, upgrade, group_name_list=[]):

    print('\n%s%s' % ('--> ', module))
    if module in cli.modules_to_upgrade:
        new_module = install.module_install_upgrade(module, True)
    else:
        new_module = install.module_install_upgrade(module, upgrade)

    # if new_module and group_name_list != []:

    #     user_name = 'Administrator'
    #     print('%s%s(%s)' % ('--> ', module, user_name))
    #     user_groups_set(user_name, group_name_list)

    #     user_name = 'Data Administrator'
    #     print('%s%s(%s)' % ('--> ', module, user_name))
        # user_groups_set(user_name, group_name_list)

    return new_module


def install_():

    global upgrade

    print('--> create_database()')
    newDB = install.create_database()
    if newDB:
        print('\n--> newDB: ', newDB)
    #     print('--> MyCompany()')
    #     MyCompany()
    #     print('--> Administrator()')
    #     Administrator()
    #     print('--> Demo_User()')
    #     Demo_User()
    #     print('--> Data_Administrator_User()')
    #     Data_Administrator_User()
    else:
        print('\n--> newDB: ', newDB)
    #     client = erppeek.Client(server,
    #                             db=dbname,
    #                             user=admin_user,
    #                             password=admin_user_pw,
    #                             verbose=False)
    #     print('--> client: ', client)
    #     proxy = client.model('ir.module.module')
    #     proxy.upgrade_list()

    # ################################################################################################################
    #
    # Odoo Addons
    #
    # ################################################################################################################

    group_names = []
    install_upgrade_module('contacts', cli.upgrade_all, group_names)

    # group_names = []
    # install_upgrade_module('mail', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('hr', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('sales_team', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('survey', upgrade, group_names)

    # ################################################################################################################
    #
    # OCA/l10n-brazil
    #
    # ################################################################################################################

    # group_names = []
    # install_upgrade_module('l10n_br_base', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('l10n_br_zip', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('l10n_br_zip_correios', upgrade, group_names)

    # ################################################################################################################
    #
    # OCA/server-tools
    #
    # ################################################################################################################

    # group_names = []
    # install_upgrade_module('mass_editing', upgrade, group_names)

    # ################################################################################################################
    #
    # CLVsol Odoo Addons
    #
    # ################################################################################################################

    # group_names = []
    # install_upgrade_module('clv_disable_web_access', upgrade, group_names)

    # group_names = [
    #     'User (Base)',
    #     'Super User (Base)',
    #     'Annotation User (Base)',
    #     'Register User (Base)',
    #     'Log User (Base)',
    #     'Manager (Base)',
    #     'Super Manager (Base)',
    # ]
    # install_upgrade_module('clv_base', upgrade, group_names)

    # group_names = [
    #     'User (Off)',
    #     'Super User (Off)',
    #     'Manager (Off)',
    #     'Super Manager (Off)',
    # ]
    # install_upgrade_module('clv_off', upgrade, group_names)

    # group_names = [
    #     'User (File System)',
    #     'Manager (File System)',
    #     'Super Manager (File System)',
    # ]
    # install_upgrade_module('clv_file_system', upgrade, group_names)

    # group_names = [
    #     'User (Global Tag)',
    #     'Manager (Global Tag)',
    #     'Super Manager (Global Tag)',
    # ]
    # install_upgrade_module('clv_global_tag', upgrade, group_names)

    # group_names = [
    #     'User (History Marker)',
    #     'Manager (History Marker)',
    #     'Super Manager (History Marker)',
    # ]
    # install_upgrade_module('clv_history_marker', upgrade, group_names)

    # group_names = [
    #     'User (Report)',
    #     'Manager (Report)',
    #     'Super Manager (Report)',
    # ]
    # install_upgrade_module('clv_report', upgrade, group_names)

    # group_names = [
    #     'User (Data Export)',
    #     'Manager (Data Export)',
    #     'Super Manager (Data Export)',
    # ]
    # install_upgrade_module('clv_data_export', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_employee', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_employee_history', upgrade, group_names)

    # group_names = [
    #     'User (Employee Management)',
    #     'Manager (Employee Management)',
    #     'Super Manager (Employee Management)',
    # ]
    # install_upgrade_module('clv_employee_mng', upgrade, group_names)

    # group_names = [
    #     'User (Address)',
    #     'Manager (Address)',
    #     'Super Manager (Address)',
    # ]
    # install_upgrade_module('clv_address', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_address_history', upgrade, group_names)

    # group_names = [
    #     'User (Person)',
    #     'Manager (Person)',
    #     'Super Manager (Person)',
    # ]
    # install_upgrade_module('clv_person', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_person_history', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_person_address_history', upgrade, group_names)

    # group_names = [
    #     'User (Person Management)',
    #     'Manager (Person Management)',
    #     'Super Manager (Person Management)',
    # ]
    # install_upgrade_module('clv_person_mng', upgrade, group_names)

    # group_names = [
    #     'User (Person Off)',
    #     'Manager (Person Off)',
    #     'Super Manager (Person Off)',
    # ]
    # install_upgrade_module('clv_person_off', upgrade, group_names)

    # group_names = [
    #     'User (Animal)',
    #     'Manager (Animal)',
    #     'Super Manager (Animal)',
    # ]
    # install_upgrade_module('clv_animal', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_animal_history', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_animal_address_history', upgrade, group_names)

    # group_names = [
    #     'User (Community)',
    #     'Manager (Community)',
    #     'Super Manager (Community)',
    # ]
    # install_upgrade_module('clv_community', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_community_history', upgrade, group_names)

    # group_names = [
    #     'User (Event)',
    #     'Manager (Event)',
    #     'Super Manager (Event)',
    # ]
    # install_upgrade_module('clv_event', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_event_history', upgrade, group_names)

    # group_names = [
    #     'User (Survey)',
    #     'Manager (Survey)',
    #     'Super Manager (Survey)',
    # ]
    # install_upgrade_module('clv_survey', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_survey_history', upgrade, group_names)

    # group_names = [
    #     'User (Lab Test)',
    #     'Manager (Lab Test)',
    #     'Super Manager (Lab Test)',
    #     'Approver (Lab Test)',
    # ]
    # install_upgrade_module('clv_lab_test', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_lab_test_history', upgrade, group_names)

    # group_names = [
    #     'User (Lab Test (Off))',
    #     'Manager (Lab Test (Off))',
    #     'Super Manager (Lab Test (Off))',
    #     'Approver (Lab Test (Off))',
    # ]
    # install_upgrade_module('clv_lab_test_off', upgrade, group_names)

    # group_names = [
    #     'User (Document)',
    #     'Manager (Document)',
    #     'Super Manager (Document)',
    #     'Approver (Document)',
    # ]
    # install_upgrade_module('clv_document', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_document_history', upgrade, group_names)

    # group_names = [
    #     'User (Document (Off))',
    #     'Manager (Document (Off))',
    #     'Super Manager (Document (Off))',
    # ]
    # install_upgrade_module('clv_document_off', upgrade, group_names)

    # group_names = [
    #     'User (Media File)',
    #     'Manager (Media File)',
    #     'Super Manager (Media File)',
    # ]
    # install_upgrade_module('clv_mfile', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_mfile_history', upgrade, group_names)

    # group_names = [
    #     'User (Summary)',
    #     'Manager (Summary)',
    #     'Super Manager (Summary)',
    # ]
    # install_upgrade_module('clv_summary', upgrade, group_names)

    # ################################################################################################################
    #
    # CLVsol Odoo Addons - Brazilian Localization
    #
    # ################################################################################################################

    # group_names = []
    # install_upgrade_module('clv_l10n_br_base', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_address_l10n_br', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_person_l10n_br', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_person_history_l10n_br', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_person_mng_l10n_br', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_person_off_l10n_br', upgrade, group_names)

    # ################################################################################################################
    #
    # CLVsol Odoo Addons - JCAFB customizations
    #
    # ################################################################################################################

    # group_names = []
    # install_upgrade_module('clv_base_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_off_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_file_system_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_global_tag_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_history_marker_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_report_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_data_export_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_employee_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_employee_mng_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_address_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_address_history_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_person_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_person_mng_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_person_history_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_person_address_history_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_person_off_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_animal_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_animal_history_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_animal_address_history_jcafb', upgrade, group_names)

    # group_names = [
    #     'User (Animal Management)',
    #     'Manager (Animal Management)',
    #     'Super Manager (Animal Management)',
    # ]
    # install_upgrade_module('clv_animal_mng', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_community_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_event_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_survey_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_survey_jcafb_2017', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_survey_jcafb_2018', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_lab_test_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_lab_test_off_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_lab_test_jcafb_2017', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_lab_test_jcafb_2018', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_document_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_document_off_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_mfile_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_summary_jcafb', upgrade, group_names)

    # group_names = []
    # install_upgrade_module('clv_default_jcafb_2018', upgrade, group_names)

    # group_names = [
    #     'User (Person Selection)',
    #     'Manager (Person Selection)',
    #     'Super Manager (Person Selection)',
    # ]
    # install_upgrade_module('clv_person_sel', upgrade, group_names)


if __name__ == '__main__':

    from time import time

    # get_arguments()
    cli = CLI(demo_data=demo_data, lang=lang, tz=tz)
    cli.get_arguments_install()

    install = Install(
        server=cli.server,
        super_user_pw=cli.super_user_pw,
        dbname=cli.dbname,
        demo_data=cli.demo_data,
        lang=cli.lang,
        admin_user_pw=cli.admin_user_pw
    )

    start = time()

    print('--> Executing install.py...\n')

    print('--> Executing install()...\n')
    install_()

    print('\n--> install.py')
    print('--> Execution time:', secondsToStr(time() - start), '\n')
