SPEC :=		libdaq.spec

ifeq ($(findstring epel-6,$(MOCK_CONFIG)),epel-6)
MOCK_INSTALL =	libnetfilter_queue-1.0.0-2 \
		libnetfilter_queue-devel-1.0.0-2
endif

include ../../mk/rpm.mk

SOURCE0_FILENAME :=	daq-$(RPM_VERSION).tar.gz
SOURCE0_URL :=		http://www.snort.org/downloads/2103

pre-fetch::
	@if [ ! -e $(DISTFILE_DIR)/$(SOURCE0_FILENAME) ]; then \
		wget -O $(DISTFILE_DIR)/$(SOURCE0_FILENAME) $(SOURCE0_URL); \
	fi
