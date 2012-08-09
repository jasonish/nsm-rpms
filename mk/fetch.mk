$(DISTFILE_DIR):
	@mkdir -p $(DISTFILE_DIR)

pre-fetch::

fetch: $(DISTFILE_DIR) pre-fetch
	spectool -g -C $(DISTFILE_DIR) $(SPEC)
	mkdir -p ./work/SOURCES
	mkdir -p $(DISTFILE_DIR)
	for f in $(SOURCES); do \
		if [ -e ./$$f ]; then \
			cp ./$$f ./work/SOURCES; \
		elif [ -e $(DISTFILE_DIR)/$$f ]; then \
			cp $(DISTFILE_DIR)/$$f ./work/SOURCES; \
		fi \
	done

$(addprefix work/SOURCES/,$(SOURCES)):
	@$(MAKE) fetch
