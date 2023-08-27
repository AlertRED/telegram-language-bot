from arq import run_worker

from .worker import WorkerSettings


if __name__ == '__main__':
    worker = run_worker(WorkerSettings)
