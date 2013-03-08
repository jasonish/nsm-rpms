SPEC =		barnyard2.spec

SOURCE_FILE =	barnyard2-$(RPM_VERSION).tar.gz
SOURCE_URL =	https://github.com/firnsy/barnyard2/tarball/v2-$(RPM_VERSION)
#SOURCE_URL =	https://github.com/jasonish/barnyard2/archive/ish/v2-1.11.tar.gz
include ../../mk/rpm.mk

pre-fetch::
	@if [ ! -e $(DISTFILE_DIR)/$(SOURCE_FILE) ]; then \
		wget -O $(DISTFILE_DIR)/$(SOURCE_FILE) $(SOURCE_URL); \
	fi
