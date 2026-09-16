from gdo.base.GDO import GDO
from gdo.base.Query import Query
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_UserName import GDT_UserName
from gdo.date.GDT_Date import GDT_Date
from gdo.table.MethodQueryTable import MethodQueryTable


class overview(MethodQueryTable):

    def gdo_table(self) -> GDO:
        return GDO_User.table()

    def gdo_table_headers(self) -> list:
        return [
            GDT_UserName('user_name').label('username'),
            GDT_Date('birthday'),
        ]

    def gdo_table_query(self) -> Query:
        return self.gdo_module().birthday_query()

    def gdo_order_default(self) -> str:
        return (
            "DATE_FORMAT(setting_birthday.uset_val, '%m-%d') < DATE_FORMAT(CURDATE(), '%m-%d') ASC, "
            "DATE_FORMAT(setting_birthday.uset_val, '%m-%d') ASC"
        )
