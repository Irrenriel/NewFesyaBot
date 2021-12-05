if __name__ == '__main__':
    from multiprocessing import Process
    from aiogram import executor
    from resources.models import dp, loop

    # The most important to write this import!
    from src import handlers


    def main():
        executor.start_polling(dp, skip_updates=True, loop=loop)