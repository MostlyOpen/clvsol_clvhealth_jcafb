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

import images

from odoo_client.cli import *
from odoo_client.install import *


class CLVhealth_JCAFB(object):

    def __init__(
        self,

        CompanyName='CLVhealth-JCAFB',
        Company_image=images.Company_image,
        website='https://github.com/CLVsol',

        admin_user_email='admin@clvsol.com',
        Administrator_image=images.Administrator_image,

        demo_user_name='Demo User',
        demo_user='demo',
        demo_user_pw='demo',
        demo_user_email='demo.user@clvsol.com',
        Demo_User_image=images.Demo_User_image,

        data_admin_user_name='Data Administrator',
        data_admin_user='data.admin',
        data_admin_user_pw='data.admin',
        data_admin_user_email='data.admin@clvsol.com',
        DataAdministrator_image=images.DataAdministrator_image,

        lang='pt_BR',
        tz='America/Sao_Paulo',

        demo_data=False,
    ):

        self.CompanyName = CompanyName
        self.Company_image = Company_image
        self.website = website

        self.admin_user_email = admin_user_email
        self.Administrator_image = Administrator_image

        self.demo_user_name = demo_user_name
        self.demo_user = demo_user
        self.demo_user_pw = demo_user_pw
        self.demo_user_email = demo_user_email
        self.Demo_User_image = Demo_User_image

        self.data_admin_user_name = data_admin_user_name
        self.data_admin_user = data_admin_user
        self.data_admin_user_pw = data_admin_user_pw
        self.data_admin_user_email = data_admin_user_email
        self.DataAdministrator_image = DataAdministrator_image

        self.lang = lang
        self.tz = tz

        self.demo_data = demo_data

    def install_upgrade_module(self, module, upgrade, group_name_list=[]):

        print('\n%s%s' % ('--> ', module))
        if module in cli.modules_to_upgrade:
            new_module = install.module_install_upgrade(module, True)
        else:
            new_module = install.module_install_upgrade(module, upgrade)

        if new_module and group_name_list != []:

            user_name = 'Administrator'
            print('\n%s%s (%s) %s' % ('--> ', module, user_name, group_name_list))
            install.user_groups_set(user_name, group_name_list)

            user_name = 'Data Administrator'
            print('\n%s%s (%s) %s' % ('--> ', module, user_name, group_name_list))
            install.user_groups_set(user_name, group_name_list)

        return new_module

    def install(self):

        global upgrade

        print('--> create_database()')
        newDB = install.create_database()
        if newDB:
            print('\n--> newDB: ', newDB)
            print('\n--> MyCompany()')
            install.MyCompany(self.CompanyName, self.website, self.Company_image)
            print('\n--> Administrator()')
            install.Administrator(self.admin_user_email, self.Administrator_image)
            print('\n--> Demo_User()')
            install.Demo_User(
                self.demo_user_name, self.demo_user_email, self.CompanyName,
                self.demo_user, self.demo_user_pw, self.Demo_User_image
            )
            print('\n--> Data_Administrator_User()')
            install.Data_Administrator_User(
                self.data_admin_user_name, self.data_admin_user_email, self.CompanyName,
                self.data_admin_user, self.data_admin_user_pw, self.DataAdministrator_image
            )
        else:
            print('\n--> newDB: ', newDB)
            client = erppeek.Client(
                server=cli.server,
                db=cli.dbname,
                user='admin',
                password=cli.admin_user_pw
            )
            print('\n--> Update Modules List"')
            IrModuleModule = client.model('ir.module.module')
            IrModuleModule.update_list()

        # ############################################################################################
        #
        # Odoo Addons
        #
        # ############################################################################################

        group_names = []
        self.install_upgrade_module('contacts', cli.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('mail', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('hr', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('sales_team', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('survey', upgrade, group_names)

        # ############################################################################################
        #
        # OCA/l10n-brazil
        #
        # ############################################################################################

        # group_names = []
        # install_upgrade_module('l10n_br_base', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('l10n_br_zip', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('l10n_br_zip_correios', upgrade, group_names)

        # ############################################################################################
        #
        # OCA/server-tools
        #
        # ############################################################################################

        # group_names = []
        # install_upgrade_module('mass_editing', upgrade, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons
        #
        # ############################################################################################

        # group_names = []
        # install_upgrade_module('clv_disable_web_access', upgrade, group_names)

        group_names = [
            'User (Base)',
            'Super User (Base)',
            'Annotation User (Base)',
            'Register User (Base)',
            'Log User (Base)',
            'Manager (Base)',
            'Super Manager (Base)',
        ]
        self.install_upgrade_module('clv_base', cli.upgrade_all, group_names)

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

        group_names = [
            'User (Global Tag)',
            'Manager (Global Tag)',
            'Super Manager (Global Tag)',
        ]
        self.install_upgrade_module('clv_global_tag', cli.upgrade_all, group_names)

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

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Brazilian Localization
        #
        # ############################################################################################

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

        # ############################################################################################
        #
        # CLVsol Odoo Addons - JCAFB customizations
        #
        # ############################################################################################

        group_names = []
        self.install_upgrade_module('clv_base_jcafb', cli.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_off_jcafb', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('clv_file_system_jcafb', upgrade, group_names)

        group_names = []
        self.install_upgrade_module('clv_global_tag_jcafb', cli.upgrade_all, group_names)

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

    clvhealth_jcafb = CLVhealth_JCAFB()

    cli = CLI(
        demo_data=clvhealth_jcafb.demo_data,
        lang=clvhealth_jcafb.lang,
        tz=clvhealth_jcafb.tz
    )
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
    clvhealth_jcafb.install()

    print('\n--> install.py')
    print('--> Execution time:', secondsToStr(time() - start), '\n')
