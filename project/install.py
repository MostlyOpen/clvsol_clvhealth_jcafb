# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import images

from odoo_client.cli import *
from odoo_client.db import *


class CLVhealthJCAFB(object):

    def __init__(
        self,

        server='http://localhost:8069',

        CompanyName='CLVhealth-JCAFB',
        Company_image=images.Company_image,
        website='https://github.com/CLVsol',

        admin_user_pw='admin',
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

        dbname='clvhealth_jcafb',

        lang='pt_BR',
        tz='America/Sao_Paulo',

        demo_data=False,
        upgrade_all=False,
        modules_to_upgrade=[],
    ):

        self.server = server

        self.CompanyName = CompanyName
        self.Company_image = Company_image
        self.website = website

        self.admin_user_pw = admin_user_pw
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

        self.dbname = dbname

        self.lang = lang
        self.tz = tz

        self.demo_data = demo_data
        self.upgrade_all = upgrade_all
        self.modules_to_upgrade = modules_to_upgrade

    def install_upgrade_module(self, module, upgrade, group_name_list=[]):

        print('\n%s%s' % ('--> ', module))
        if module in self.modules_to_upgrade:
            new_module = db.module_install_upgrade(module, True)
        else:
            new_module = db.module_install_upgrade(module, upgrade)

        if new_module and group_name_list != []:

            user_name = 'Administrator'
            print('\n%s%s (%s) %s' % ('--> ', module, user_name, group_name_list))
            db.user_groups_setup(user_name, group_name_list)

            user_name = 'Data Administrator'
            print('\n%s%s (%s) %s' % ('--> ', module, user_name, group_name_list))
            db.user_groups_setup(user_name, group_name_list)

        return new_module

    def install(self):

        global upgrade

        print('--> create_database()')
        newDB = db.create()
        if newDB:
            print('\n--> newDB: ', newDB)
            print('\n--> my_company_setup()')
            db.my_company_setup(self.CompanyName, self.website, self.Company_image)
            print('\n--> Administrator()')
            db.administrator_setup(self.admin_user_email, self.Administrator_image)
            print('\n--> demo_user_setup()')
            db.demo_user_setup(
                self.demo_user_name, self.demo_user_email, self.CompanyName,
                self.demo_user, self.demo_user_pw, self.Demo_User_image
            )
            print('\n--> data_administrator_user_setup()')
            db.data_administrator_user_setup(
                self.data_admin_user_name, self.data_admin_user_email, self.CompanyName,
                self.data_admin_user, self.data_admin_user_pw, self.DataAdministrator_image
            )
        else:
            print('\n--> newDB: ', newDB)
            client = erppeek.Client(
                server=self.server,
                db=self.dbname,
                user='admin',
                password=self.admin_user_pw
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
        self.install_upgrade_module('contacts', False, group_names)

        # group_names = []
        # install_upgrade_module('mail', upgrade, group_names)

        group_names = []
        self.install_upgrade_module('hr', False, group_names)

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
        self.install_upgrade_module('clv_base', self.upgrade_all, group_names)

        # group_names = [
        #     'User (Off)',
        #     'Super User (Off)',
        #     'Manager (Off)',
        #     'Super Manager (Off)',
        # ]
        # install_upgrade_module('clv_off', upgrade, group_names)

        group_names = []
        self.install_upgrade_module('clv_mass_editing', self.upgrade_all, group_names)

        group_names = [
            'User (File System)',
            'Manager (File System)',
            'Super Manager (File System)',
        ]
        self.install_upgrade_module('clv_file_system', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_global_log', self.upgrade_all, group_names)

        group_names = [
            'User (Global Tag)',
            'Manager (Global Tag)',
            'Super Manager (Global Tag)',
        ]
        self.install_upgrade_module('clv_global_tag', self.upgrade_all, group_names)

        group_names = [
            'User (Phase)',
            'Manager (Phase)',
            'Super Manager (Phase)',
        ]
        self.install_upgrade_module('clv_phase', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_entity', self.upgrade_all, group_names)

        # group_names = [
        #     'User (Report)',
        #     'Manager (Report)',
        #     'Super Manager (Report)',
        # ]
        # install_upgrade_module('clv_report', upgrade, group_names)

        group_names = [
            'User (External Sync)',
            'Manager (External Sync)',
            'Super Manager (External Sync)',
        ]
        self.install_upgrade_module('clv_external_sync', self.upgrade_all, group_names)

        group_names = [
            'User (Export)',
            'Manager (Export)',
            'Super Manager (Export)',
        ]
        self.install_upgrade_module('clv_export', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_employee', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_employee_history', upgrade, group_names)

        # group_names = [
        #     'User (Employee Management)',
        #     'Manager (Employee Management)',
        #     'Super Manager (Employee Management)',
        # ]
        # install_upgrade_module('clv_employee_mng', upgrade, group_names)

        group_names = [
            'User (Address)',
            'Manager (Address)',
            'Super Manager (Address)',
        ]
        self.install_upgrade_module('clv_address', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_address_history', upgrade, group_names)

        group_names = [
            'User (Patient)',
            'Manager (Patient)',
            'Super Manager (Patient)',
        ]
        self.install_upgrade_module('clv_patient', self.upgrade_all, group_names)

        group_names = [
            'User (Person)',
            'Manager (Person)',
            'Super Manager (Person)',
        ]
        self.install_upgrade_module('clv_person', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_person_history', self.upgrade_all, group_names)

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

        group_names = [
            'User (Animal)',
            'Manager (Animal)',
            'Super Manager (Animal)',
        ]
        self.install_upgrade_module('clv_animal', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_animal_history', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('clv_animal_address_history', upgrade, group_names)

        group_names = [
            'User (Community)',
            'Manager (Community)',
            'Super Manager (Community)',
        ]
        self.install_upgrade_module('clv_community', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_community_history', upgrade, group_names)

        group_names = [
            'User (Event)',
            'Manager (Event)',
            'Super Manager (Event)',
        ]
        self.install_upgrade_module('clv_event', self.upgrade_all, group_names)

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

        group_names = [
            'User (Lab Test)',
            'Manager (Lab Test)',
            'Super Manager (Lab Test)',
            'Approver (Lab Test)',
        ]
        self.install_upgrade_module('clv_lab_test', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_lab_test_history', upgrade, group_names)

        # group_names = [
        #     'User (Lab Test (Off))',
        #     'Manager (Lab Test (Off))',
        #     'Super Manager (Lab Test (Off))',
        #     'Approver (Lab Test (Off))',
        # ]
        # install_upgrade_module('clv_lab_test_off', upgrade, group_names)

        group_names = [
            'User (Document)',
            'Manager (Document)',
            'Super Manager (Document)',
            'Approver (Document)',
        ]
        self.install_upgrade_module('clv_document', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_document_history', self.upgrade_all, group_names)

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
        self.install_upgrade_module('clv_base_jcafb', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_off_jcafb', upgrade, group_names)

        group_names = []
        self.install_upgrade_module('clv_file_system_jcafb', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_global_log_jcafb', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_global_tag_jcafb', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_phase_jcafb', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_report_jcafb', upgrade, group_names)

        group_names = []
        self.install_upgrade_module('clv_external_sync_jcafb', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_export_jcafb', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_employee_jcafb', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('clv_employee_mng_jcafb', upgrade, group_names)

        group_names = []
        self.install_upgrade_module('clv_address_jcafb', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_address_sync_jcafb', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_address_history_jcafb', upgrade, group_names)

        group_names = []
        self.install_upgrade_module('clv_patient_jcafb', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_person_jcafb', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_person_sync_jcafb', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_person_mng_jcafb', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('clv_person_history_jcafb', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('clv_person_address_history_jcafb', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('clv_person_off_jcafb', upgrade, group_names)

        group_names = []
        self.install_upgrade_module('clv_animal_jcafb', self.upgrade_all, group_names)

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

        group_names = []
        self.install_upgrade_module('clv_community_jcafb', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_event_jcafb', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_survey_jcafb', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('clv_survey_jcafb_2017', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('clv_survey_jcafb_2018', upgrade, group_names)

        group_names = []
        self.install_upgrade_module('clv_lab_test_jcafb', self.upgrade_all, group_names)

        # group_names = []
        # install_upgrade_module('clv_lab_test_off_jcafb', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('clv_lab_test_jcafb_2017', upgrade, group_names)

        # group_names = []
        # install_upgrade_module('clv_lab_test_jcafb_2018', upgrade, group_names)

        group_names = []
        self.install_upgrade_module('clv_document_jcafb', self.upgrade_all, group_names)

        group_names = []
        self.install_upgrade_module('clv_document_sync_jcafb', self.upgrade_all, group_names)

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

    cli = CLI(
        super_user_pw='*',
        admin_user_pw='*',
        data_admin_user_pw='*',
        dbname='*',
        demo_data=False,
        lang='pt_BR',
        tz='America/Sao_Paulo',
    )
    cli.argparse_db_setup()

    clvhealth_jcafb = CLVhealthJCAFB(
        # super_user_pw=cli.super_user_pw,
        admin_user_pw=cli.admin_user_pw,
        demo_user_pw='demo',
        data_admin_user_pw=cli.data_admin_user_pw,
        demo_data=cli.demo_data,
        upgrade_all=cli.upgrade_all,
        modules_to_upgrade=cli.modules_to_upgrade,
        lang=cli.lang,
        tz=cli.tz
    )

    db = DB(
        server=cli.server,
        super_user_pw=cli.super_user_pw,
        admin_user_pw=cli.admin_user_pw,
        data_admin_user_pw=cli.data_admin_user_pw,
        dbname=cli.dbname,
        demo_data=cli.demo_data,
        lang=cli.lang,
        tz=cli.tz
    )

    start = time()

    print('--> Executing install.py...\n')

    print('--> Executing install()...\n')
    clvhealth_jcafb.install()

    print('\n--> install.py')
    print('--> Execution time:', secondsToStr(time() - start), '\n')
