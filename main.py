import logging
import subprocess
import json
from telegram.ext import Updater, CommandHandler

TELEGRAM_TOKEN = "1411158690:AAH51GDxqh33p3SOsh4eRPbiB3ySIlQJq98"


# TEST_CHAT_ID = 615260998


class BotController:
    config_file_name = "config.json"

    def load_config(self):
        try:
            with open(self.config_file_name) as f:
                self._config = json.loads(f)
        except FileNotFoundError:
            pass

    def save_config(self):
        with open(self.config_file_name, "w") as f:
            json.dump(self._config, f, indent=2)

    def __init__(self, telegram_bot_token):
        self._config = {}

        self._telegram_updater = Updater(TELEGRAM_TOKEN, use_context=True)
        self._add_commands()
        self.load_config()

    def _add_commands(self):
        self._telegram_updater.dispatcher.add_handler(CommandHandler("start", self._start, pass_args=True))
        self._telegram_updater.dispatcher.add_handler(CommandHandler("stop", self._stop, pass_args=True))
        self._telegram_updater.dispatcher.add_handler(CommandHandler("setDefaultTime", self._stop, pass_args=True))
        self._telegram_updater.dispatcher.add_handler(CommandHandler("setDefaultVol", self._stop, pass_args=True))
        self._telegram_updater.dispatcher.add_handler(CommandHandler("showConfig", self._print_config, pass_args=True))
        self._telegram_updater.dispatcher.add_handler(CommandHandler("help", self.help, pass_args=True))

    def help(self, update, context):
        help_string_builder = []
        for cmd in self._telegram_updater.dispatcher.handlers[0]:
            help_string_builder.append(cmd.command[0])
        print("adsadas", help_string_builder)
        update.message.reply_text("/" + "\n/".join(help_string_builder))


    def _set_default_time(self, update, context):
        if len(context) == 1:
            self._config["time"] = context[0]
        self.save_config()

    def _set_default_vol(self, update, context):
        if len(context) == 1:
            self._config["vol"] = context[0]
        self.save_config()

    def _print_config(self, update, context):
        update.message.reply_text(self._config)

    def start(self):
        self._telegram_updater.start_polling()
        self._telegram_updater.idle()

    def _stop(self):
        self._sound_subprocess.kill()

    def _start(self):
        self._sound_subprocess = subprocess.Popen("mpg123 /home/pi/12500.mp3", shell=True)


def main():
    logging.basicConfig(level=logging.DEBUG)
    bot_controller = BotController(TELEGRAM_TOKEN)
    bot_controller.start()


if __name__ == "__main__":
    main()
    # test()
