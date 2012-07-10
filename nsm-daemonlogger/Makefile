SPEC :=		nsm-daemonlogger.spec

include ../mk/rpm.mk

SOURCE0_FILENAME :=	daemonlogger-1.2.1.tar.gz
SOURCE0_URL :=		http://www.snort.org/downloads/463

pre-fetch::
	@if [ ! -e $(DISTFILE_DIR)/$(SOURCE0_FILENAME) ]; then \
		wget -O $(DISTFILE_DIR)/$(SOURCE0_FILENAME) $(SOURCE0_URL); \
	fi
