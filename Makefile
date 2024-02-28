include module.spec
BUILD_DIR ?= build
C_VERSION ?= develop
REL = $(BUILD_DIR)/rel
PANEL = $(REL)/panel
SERVER = $(REL)/server

.PHONY: all

all: archive

client:
	@echo "Getting Xabber Web client ..."
	@if [ ! -d "$(BUILD_DIR)/xabber_web" ]; then \
		mkdir -p $(BUILD_DIR)/xabber_web ;\
		cd $(BUILD_DIR)/xabber_web ;\
		git init -q ;\
		git remote add origin https://github.com/redsolution/xabber-web.git ;\
	fi
	@cd $(BUILD_DIR)/xabber_web && git fetch && git checkout $(C_VERSION); git pull origin $(C_VERSION)


mkdirs:
	@if [ ! -d "$(BUILD_DIR)" ]; then  mkdir $(BUILD_DIR);fi
	@if [ ! -d "$(REL)" ]; then  mkdir $(REL);fi
	@if [ ! -d "$(PANEL)" ]; then  mkdir $(PANEL);fi
	@if [ ! -d "$(SERVER)" ]; then  mkdir $(SERVER);fi

static:
	@echo -n "Collect static ..."
	@cp -r xabber_web  $(PANEL)/ && echo -n "."
	@cp -r module.spec $(REL)/ && echo -n "."
	@mkdir -p $(PANEL)/xabber_web/static/xabberweb
	@cp -r $(BUILD_DIR)/xabber_web/dist  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@cp -r $(BUILD_DIR)/xabber_web/assets  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@cp -r $(BUILD_DIR)/xabber_web/manifest.json  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@cp -r $(BUILD_DIR)/xabber_web/firebase-messaging-sw.js  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@WEB_VER=$$(grep \"version_number\" $(BUILD_DIR)/xabber_web/version.js | sed -n "s/.*\"version_number\":\(\S*\),.*$$/\1/p");\
	sed -r "s/^(XABBER_WEB_VER =).*/\1 $$WEB_VER/" xabber_web/config.py > $(PANEL)/xabber_web/config.py
	@echo ". done."


archive: mkdirs client static
	@echo -n "Make archive ..."
	@cd $(REL) && tar -czf "../module_$(NAME)_$(VERSION).tar.gz" panel server module.spec
	@echo ". done."

clean:
	rm -rf $(BUILD_DIR)
