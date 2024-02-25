import os
import logging
import multiprocessing
import threading
import time
import json

from server.launch import uvicorn_run
from module.object_count_algorithm import ObjectCounter
from module.connection import commit_data

CONFIG = json.loads(open("config.json").read())

def init_logging_format():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')


def start_uvicorn_process():
    init_logging_format()
    logging.warning(f"Server process (PID: {os.getpid()}) is starting...")

    uvicorn_run(PORT=CONFIG["PORT"])

    logging.warning(f"Server process (PID: {os.getpid()}) disconnected...")


# def start_module_process(VIDEO_SOURCE, DATABASE_TABLE):
#     init_logging_format()
#     logging.warning(f"Module process (PID: {os.getpid()}) is starting...")
#
#     tracker = ObjectCounter(VIDEO_SOURCE)
#     tracker_thread = threading.Thread(target=tracker.run)
#
#     db_connect_thread = threading.Thread(target=commit_data,
#                                          args=(tracker, DATABASE_TABLE),
#                                          daemon=True
#                                          )
#
#     tracker_thread.start()
#     logging.warning(f"Module, Tracker thread (PID: {os.getpid()}, TID: {tracker_thread.ident}) is starting...")
#     time.sleep(1)
#
#     db_connect_thread.start()
#     logging.warning(f"Module, DB-Conn thread (PID: {os.getpid()}, TID: {db_connect_thread.ident}) is starting...")
#
#     tracker_thread.join()
#     logging.warning(f"Module process (PID: {os.getpid()}) disconnected...")


if __name__ == "__main__":
    multiprocessing.freeze_support()

    init_logging_format()
    logging.warning("Parent process (PID: {}) is starting...".format(os.getpid()))


    # VIDEO_SOURCE_1 = CONFIG["VIDEO_SOURCE"]["1"]
    # VIDEO_SOURCE_2 = CONFIG["VIDEO_SOURCE"]["2"]
    #
    # DATABASE_TABLE_1 = CONFIG["DATABASE_TABLE"]["1"]
    # DATABASE_TABLE_2 = CONFIG["DATABASE_TABLE"]["2"]

    server_process = multiprocessing.Process(target=start_uvicorn_process)
    # module_process_1 = multiprocessing.Process(target=start_module_process,
    #                                            args=(VIDEO_SOURCE_1, DATABASE_TABLE_1),
    #                                            daemon=True
    #                                            )
    # module_process_2 = multiprocessing.Process(target=start_module_process,
    #                                            args=(VIDEO_SOURCE_2, DATABASE_TABLE_2),
    #                                            daemon=True
    #                                            )

    server_process.start()
    # module_process_1.start()
    # module_process_2.start()

    server_process.join()
    # module_process_1.join()
    # module_process_2.join()
