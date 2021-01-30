import logging
from telegram.ext import Updater, CommandHandler

TELEGRAM_TOKEN = "902632494:AAF99gqLSl4lZI05f0XASrNmtHGQsdtrL3Y"

TEST_CHAT_ID = 615260998
    
class BotController:
    def __init__(self, telegram_bot_token):
        self._telegram_updater = Updater(TELEGRAM_TOKEN, use_context=True)
        self._add_commands()

    def _add_commands(self):
        self._telegram_updater.dispatcher.add_handler(CommandHandler("info", self.info, pass_args=True))
    
    def start(self):
        self._telegram_updater.start_polling()
        self._telegram_updater.idle()

    def info(self, update, context):
        symbol = context.args[0]
        print(symbol)
        # replay = yaml.dump(self._stocks_manager.get_stock_info(symbol))
        # update.message.reply_text(replay)

def main():
    logging.basicConfig(level=logging.DEBUG)
    bot_controller = BotController(TELEGRAM_TOKEN)
    bot_controller.start()


if __name__ == "__main__":
    main()
    # test()