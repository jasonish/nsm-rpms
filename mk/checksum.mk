makesum:
ifdef SOURCES
	@echo "===> Writing checksums"
	@cd ./work/SOURCES && md5sum $(SOURCES) > $(CURDIR)/checksums
endif

checksum:
ifdef SOURCES
	@echo "===> Verifying checksums"
	@cd ./work/SOURCES && md5sum -c $(CURDIR)/checksums
endif
