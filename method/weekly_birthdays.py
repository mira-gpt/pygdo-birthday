from gdo.base.GDT import GDT
from gdo.base.Trans import tiso
from gdo.core.GDO_User import GDO_User
from gdo.core.MethodCronjob import MethodCronjob
from gdo.mail.Mail import Mail


class weekly_birthdays(MethodCronjob):

    def gdo_run_at(self) -> str:
        return '0 8 * * MON'

    def gdo_execute(self) -> GDT:
        birthdays = self.gdo_module().upcoming_birthdays()
        if not birthdays:
            return self.empty()
        names = ', '.join(user.render_name() for user in birthdays)
        query = GDO_User.table().select().only_select('gdo_user.*')
        GDO_User.join_setting(query, 'email_me_birthdays')
        query.where("email_me_birthdays='1'")
        for user in query.exec():
            if email := user.get_mail():
                iso = user.get_lang_iso() or 'en'
                Mail.from_bot().recipient(email, user.get_displayname()).subject(
                    tiso(iso, 'birthday_mail_subject')
                ).body(tiso(iso, 'birthday_mail_body', (names,))).send()
        return self.empty()
