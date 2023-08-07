.PHONY: postgres
postgres:
	sudo systemctl start postgresql

.PHONY: redis
redis:
	sudo systemctl start redis

.PHONY: rq
rq: redis
	source venv/bin/activate && rq worker --with-scheduler

.PHONY: web
web: postgres redis
	./venv/bin/python3 admin.py

.PHONY: bot
bot: postgres redis rq
	./venv/bin/python3 run.py

.PHONY: all
all: 
	make -j 3 postgres redis rq web bot