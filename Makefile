VERSION := $(shell grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3)
PATH := "/opt/bin:/opt/sbin:/home/root/.local/bin:/opt/bin:/opt/sbin:/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin"

define SCRIPT
export PATH=${PATH}
if ! type pip &> /dev/null; then
    if ! type opkg &> /dev/null; then
        echo "Opkg not found, please install toltec"
        exit 1
    fi
    opkg update
    opkg install python3-pip
fi
pip install --force-reinstall /tmp/launcherctl-${VERSION}-py3-none-any.whl
endef
export SCRIPT

ifeq ($(VENV_BIN_ACTIVATE),)
VENV_BIN_ACTIVATE := .venv/bin/activate
endif


dist/launcherctl-${VERSION}.tar.gz: $(shell find launcherctl -type f)
	python -m build --sdist

dist/launcherctl-${VERSION}-py3-none-any.whl: $(shell find launcherctl -type f)
	python -m build --wheel

clean:
	git clean --force -dX

deploy: dist/launcherctl-${VERSION}-py3-none-any.whl
	rsync dist/launcherctl-${VERSION}-py3-none-any.whl root@10.11.99.1:/tmp

install: deploy
	echo -e "$$SCRIPT" | ssh root@10.11.99.1 bash -le

test: install
	cat test.py \
	| ssh root@10.11.99.1 \
	  "bash -ec 'PATH=${PATH} /opt/bin/python -u'"

$(VENV_BIN_ACTIVATE):
	@echo "Setting up development virtual env in .venv"
	python -m venv .venv
	. $(VENV_BIN_ACTIVATE); \
	python -m pip install ruff

lint: $(VENV_BIN_ACTIVATE)
	. $(VENV_BIN_ACTIVATE); \
	python -m ruff check

lint-fix: $(VENV_BIN_ACTIVATE)
	. $(VENV_BIN_ACTIVATE); \
	python -m ruff check

format: $(VENV_BIN_ACTIVATE)
	. $(VENV_BIN_ACTIVATE); \
	python -m ruff format --diff

format-fix: $(VENV_BIN_ACTIVATE)
	. $(VENV_BIN_ACTIVATE); \
	python -m ruff format

.PHONY: clean install test deploy lint lint-fix format format-fix
