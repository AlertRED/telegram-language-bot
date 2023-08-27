.PHONY: postgres
postgres:
	sudo systemctl start postgresql

.PHONY: redis
redis:
	sudo systemctl start redis

.PHONY: rq
rq: redis
	./venv/bin/python3 -m arq scheduler.worker.WorkerSettings

.PHONY: web
web: postgres redis
	./venv/bin/python3 -m web

.PHONY: bot
bot: postgres redis rq
	./venv/bin/python3 -m bot

.PHONY: all
all: 
	make -j 3 postgres redis rq web bot