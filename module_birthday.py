from __future__ import annotations

from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Query import Query
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Bool import GDT_Bool
from gdo.date.GDT_Date import GDT_Date
from gdo.date.Time import Time
from gdo.ui.GDT_Link import GDT_Link
from gdo.ui.GDT_PageLocation import GDT_PageLocation

from datetime import timedelta

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gdo.ui.GDT_Page import GDT_Page


class module_birthday(GDO_Module):

    def gdo_dependencies(self) -> list:
        return ['date', 'mail', 'table', 'ui', 'user']

    def gdo_classes(self) -> list[type[GDO]]:
        return []

    async def gdo_install(self):
        pass

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_PageLocation('birthday_position').not_null().initial('_none'),
        ]

    def gdo_user_config(self) -> list[GDT]:
        return []

    def gdo_user_settings(self) -> list[GDT]:
        return [
            GDT_Date('birthday'),
            GDT_Bool('email_me_birthdays').not_null().initial('0'),
            GDT_Bool('announce_my_birthday').not_null().initial('0'),
        ]

    def birthday_query(self) -> Query:
        query = GDO_User.table().select().only_select('gdo_user.*')
        GDO_User.join_setting(query, 'birthday')
        GDO_User.join_setting(query, 'announce_my_birthday')
        query.where("setting_birthday.uset_val IS NOT NULL")
        query.where("setting_announce_my_birthday.uset_val='1'")
        return query

    def upcoming_birthdays(self, days: int = 7) -> list[GDO_User]:
        today = Time.get_datetime().date()
        dates = {(today + timedelta(days=day)).strftime('%m-%d') for day in range(days)}
        return [
            user for user in self.birthday_query().exec()
            if (birthday := user.gdo_val('birthday')) and birthday[5:] in dates
        ]

    def upcoming_birthday_count(self, days: int = 7) -> int:
        return len(self.upcoming_birthdays(days))

    def gdo_init(self):
        pass

    def gdo_load_scripts(self, page: 'GDT_Page'):
        self.add_js('js/pygdo-birthday.js')
        self.add_css('css/pygdo-birthday.css')

    def gdo_init_sidebar(self, page: 'GDT_Page'):
        if page_bar := self.get_config_value('birthday_position'):
            page_bar.add_field(
                GDT_Link().href(self.href('overview')).text('birthday_count', (self.upcoming_birthday_count(),)).icon('cake')
            )
