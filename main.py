if __name__ == '__main__':
    from multiprocessing import Process
    from aiogram import executor, Dispatcher
    from resources.models import dp_1, dp_2, loop

    # The most important to write this import!
    from src import handlers

    # If you are using 2 or more bots, add all their dispatchers here
    dp_pools = [dp_1, dp_2]

    def run_dispatcher(dp: Dispatcher):
        executor.start_polling(dp, skip_updates=True, loop=loop)

    processes = []
    for dp in dp_pools:
        processes.append(Process(target=run_dispatcher, args=dp))

    for i in processes:
        i.start()