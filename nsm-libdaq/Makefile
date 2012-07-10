SPEC :=		libdaq.spec

ifeq ($(findstring epel-6,$(MOCK_CONFIG)),epel-6)
MOCK_INSTALL =	libnetfilter_queue-1.0.0-2 \
		libnetfilter_queue-devel-1.0.0-2
endif

include ../mk/rpm.mk
