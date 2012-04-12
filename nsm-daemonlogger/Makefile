SPEC :=		nsm-daemonlogger.spec

include ../mk/rpm.mk

SOURCE_FILE :=	daemonlogger-$(VERSION).tar.gz

$(SOURCE_FILE):
	wget -O $@ http://www.snort.org/downloads/463

clean::
	rm -f $(SOURCE_FILE)
