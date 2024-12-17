install:
	python3 -m venv .venv
	( \
	. .venv/bin/activate; \
	pip install -r requirements.txt; \
	)

run:
	( \
	. .venv/bin/activate; \
	)

	gunicorn -c config.py service:app

test:
	( \
	. .venv/bin/activate; \
	)

	python3 client.py -f0=200 -f1=600 -d=7.5 -a=20000
	python3 client.py -f0=500.0 -d=5 -a=30000
