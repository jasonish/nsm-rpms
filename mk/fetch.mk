pre-fetch::

fetch: pre-fetch
	@spectool -g -C $(DISTFILE_DIR) $(SPEC)
	@mkdir -p ./work/SOURCES
	@for f in $(SOURCES); do \
		if [ -e ./$$f ]; then \
			cp ./$$f ./work/SOURCES; \
		elif [ -e $(DISTFILE_DIR)/$$f ]; then \
			cp $(DISTFILE_DIR)/$$f ./work/SOURCES; \
		fi \
	done

$(addprefix SOURCES/,$(SOURCES)):
	@$(MAKE) fetch
