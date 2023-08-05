from pathos.multiprocessing import ProcessPool
from tqdm import tqdm

class SuccessiveInvoker:
    def __init__(self, *commands):
        self._commands = commands

    def execute_commands(self, init_data):
        if type(init_data) == list:
            pool = ProcessPool()
            processed = []
            with tqdm(total=len(init_data)) as pbar:
                for p in pool.imap(self._process_single, init_data):
                    processed.append(p)
                    pbar.update(1)
            pool.close()
            pool.join()
            pool.clear() # Necessary to prevent current pool from being reused.
            return processed
        else:
            self._process_single(init_data)

    def _process_single(self, init_data_single):
        succession = init_data_single
        for command in self._commands:
            succession = command.execute(succession)
