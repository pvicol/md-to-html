.PHONY: clean
clean:
	find . -name \*.pyc -delete
	rm -rf public/ bin/ include/ lib/ pyvenv.cfg __pycache__

.PHONY: install
install:
	python -m venv .
	. bin/activate && pip install -r requirements.txt

.PHONY: test
test:
	. bin/activate && python -m unittest discover -s src

.PHONY: lint
lint:
	. bin/activate && flake8 src/

.PHONY: generate-site
generate-site:
	. bin/activate && python src/main.py

.PHONY: start-server
start-server:
	. bin/activate && ./main.sh

.PHONY: docker-build
docker-build: generate-site
	docker build -t staticsite .
