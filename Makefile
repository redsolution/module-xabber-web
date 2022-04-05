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
	@cd $(BUILD_DIR)/xabber_web && git pull -q origin $(C_VERSION) && git checkout $(C_VERSION)


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
	@cp -r $(BUILD_DIR)/xabber_web/fonts  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@cp -r $(BUILD_DIR)/xabber_web/images  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@cp -r $(BUILD_DIR)/xabber_web/sounds  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@cp -r $(BUILD_DIR)/xabber_web/translations  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@cp -r $(BUILD_DIR)/xabber_web/manifest.json  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@cp -r $(BUILD_DIR)/xabber_web/firebase-messaging-sw.js  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@cp -r $(BUILD_DIR)/xabber_web/background-images.xml  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@cp -r $(BUILD_DIR)/xabber_web/background-patterns.xml  $(PANEL)/xabber_web/static/xabberweb/ && echo -n "."
	@echo ". done."


archive: mkdirs client static
	@echo -n "Make archive ..."
	@cd $(REL) && tar -czf "../module_$(NAME)_$(VERSION).tar.gz" panel server module.spec
	@echo ". done."

clean:
	rm -rf $(BUILD_DIR)
