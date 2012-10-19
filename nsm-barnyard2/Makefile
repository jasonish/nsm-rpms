SPEC =		nsm-barnyard2.spec

SOURCE_FILE =	barnyard2-1.10.tar.gz
SOURCE_URL =	https://github.com/firnsy/barnyard2/tarball/v2-1.10

include ../mk/rpm.mk

pre-fetch::
	@if [ ! -e $(DISTFILE_DIR)/$(SOURCE_FILE) ]; then \
		wget -O $(DISTFILE_DIR)/$(SOURCE_FILE) $(SOURCE_URL); \
	fi
