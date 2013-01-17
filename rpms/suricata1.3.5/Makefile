SPEC :=		suricata.spec

ifeq ($(findstring epel-6,$(MOCK_CONFIG)),epel-6)
DEPENDS +=	libnetfilter_queue \
		libnetfilter_queue-devel
endif

include ../../mk/rpm.mk
