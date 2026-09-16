import os
import unittest

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.birthday.module_birthday import module_birthday
from gdo.birthday.method.weekly_birthdays import weekly_birthdays
from gdotest.TestUtil import cli_plug, reinstall_module, cli_gizmore, GDOTestCase, WebPlug, install_module, web_plug


class module_birthday_Test(GDOTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        loader = ModuleLoader.instance()
        install_module('birthday')
        loader.load_modules_db(True)
        WebPlug.COOKIES = {}
        Application.init_cli()
        loader.init_modules(True, True)
        loader.init_cli()

    def test_00_reinstall(self):
        reinstall_module('birthday')
        self.assertIs(type(module_birthday.instance()), module_birthday, "Cannot re-install module birthday.")

    def test_03_overview_cli(self):
        giz =  cli_gizmore()
        out = cli_plug(giz, "$birthday.overview")
        self.assertIsNotNone(out, '$birthday.overview does not work.')

    def test_04_weekly_cron_and_settings(self):
        module = module_birthday.instance()
        self.assertEqual('0 8 * * MON', weekly_birthdays().gdo_run_at())
        self.assertEqual('_right_bar', module.get_config_val('birthday_position'))
        self.assertEqual(
            ['birthday', 'email_me_birthdays', 'announce_my_birthday'],
            [gdt.get_name() for gdt in module.gdo_user_settings()],
        )

    def test_02_overview_web(self):
        giz =  cli_gizmore()
        out = web_plug("birthday.overview.html")
        self.assertIsNotNone(out, 'birthday.overview.html does not work.')


if __name__ == '__main__':
    unittest.main()
