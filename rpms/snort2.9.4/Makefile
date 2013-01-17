SPEC =		snort.spec

DEPENDS +=	nsm-daq

ifeq ($(findstring epel-6,$(MOCK_CONFIG)),epel-6)
DEPENDS +=	libnetfilter_queue \
		libnetfilter_queue-devel
endif

include ../../mk/rpm.mk

SOURCE0_FILENAME :=	snort-$(RPM_VERSION).tar.gz
SOURCE0_URL :=		http://www.snort.org/downloads/2112

pre-fetch::
	@if [ ! -e $(DISTFILE_DIR)/$(SOURCE0_FILENAME) ]; then \
		wget -O $(DISTFILE_DIR)/$(SOURCE0_FILENAME) $(SOURCE0_URL); \
	fi
