import logging
import subprocess
import json
from telegram.ext import Updater, CommandHandler

TELEGRAM_TOKEN = "1411158690:AAH51GDxqh33p3SOsh4eRPbiB3ySIlQJq98"

class BotController:
    """
    class that handle for taking care of all the bot commands
    """

    #  configuration file name
    config_file_name = "config.json"

    def load_config(self):
        """
        load the content of the configuration file to the config dictionary
        """
        try:
            with open(self.config_file_name) as f:
                self._config = json.loads(f)

        # if json file does not exists do not load anything and
        # create it again at the next righting to the configuration
        except FileNotFoundError:
            pass

    def save_config(self):
        with open(self.config_file_name, "w") as f:
            json.dump(self._config, f, indent=2)

    def __init__(self, telegram_bot_token):
        self._config = {}

        # object which acess to the telegram api and recognized new commands
        self._telegram_updater = Updater(TELEGRAM_TOKEN, use_context=True)
        self._add_commands()
        self.load_config()

    def _add_commands(self):
        """
        add commands to the bot
        the pass_args means that values after the command name also transfer
        in order to use commands parameters

        for example:
            /start <time> <volume>
        """

        self._telegram_updater.dispatcher.add_handler(CommandHandler("start", self._start, pass_args=True))
        self._telegram_updater.dispatcher.add_handler(CommandHandler("stop", self._stop, pass_args=True))
        self._telegram_updater.dispatcher.add_handler(
            CommandHandler("setDefaultTime", self._set_default_vol, pass_args=True))
        self._telegram_updater.dispatcher.add_handler(
            CommandHandler("setDefaultVol", self._set_default_time, pass_args=True))
        self._telegram_updater.dispatcher.add_handler(CommandHandler("showConfig", self._print_config, pass_args=True))
        self._telegram_updater.dispatcher.add_handler(CommandHandler("help", self.help, pass_args=True))

    def help(self, update, context):
        """
        show help message to the user

        the function iterate over all the commands that define in the handlers of
        telegram_updater and print them with "/" at the beginning

        :param update: telegram object for sending response message
        :param context: telegram object for sending getting commands parameters
        """

        help_string_builder = []
        for cmd in self._telegram_updater.dispatcher.handlers[0]:
            help_string_builder.append(cmd.command[0])
        update.message.reply_text("/" + "\n/".join(help_string_builder))

    def _set_volume(self, vol):
        """
        set the volume of the raspberry.

        using the shell command:
             amixer -q -M sset Headphone {vol}%

        :param vol: the volume to change to, can be from 0 to 85
        :return: the volume that changed to
        """
        try:
            vol = int(vol)

        # todo: print error to the user
        except ValueError:
            logging.error("enter number")

        if vol < 0:
            vol = 0
        elif vol > 85:
            vol = 85

        subprocess.call(f"amixer -q -M sset Headphone {vol}%")
        return vol

    def _set_default_time(self, update, context):
        if len(context.args) == 1:
            self._config["time"] = context.args[0]
        self.save_config()

    def _set_default_vol(self, update, context):
        if len(context.args) == 1:
            vol = self._set_volume(context.args[0])
            self._config["vol"] = vol
        self.save_config()

    def _print_config(self, update, context):
        """
        print the configuration to the user
        """
        update.message.reply_text(self._config)

    def start(self):
        self._telegram_updater.start_polling()
        self._telegram_updater.idle()

    def _stop(self, update, context):
        self._sound_subprocess.kill()

    def _start(self, update, context):
        time = self._config["time"]
        try:
            time = context.args[0]
        except KeyError:
            pass

        try:
            vol = context.args[1]
            self._set_volume(vol)
        except KeyError:
            pass

        self._sound_subprocess = subprocess.Popen(f"mpg123 /home/pi/12500.mp3 --timeout {time}", shell=True)


def main():
    logging.basicConfig(level=logging.DEBUG)
    bot_controller = BotController(TELEGRAM_TOKEN)
    bot_controller.start()


if __name__ == "__main__":
    main()
