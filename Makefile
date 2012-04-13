SUBDIRS +=	nsm-release-el-6

SUBDIRS +=	libnetfilter_queue

SUBDIRS +=	nsm-suricata1.2
SUBDIRS +=	nsm-suricata-latest
SUBDIRS +=	nsm-suricata-select

SUBDIRS +=	nsm-libdaq
SUBDIRS +=	nsm-snort2.9.2.1
SUBDIRS +=	nsm-snort2.9.2.2
SUBDIRS +=	nsm-snort-latest
SUBDIRS +=	nsm-snort-select

SUBDIRS +=	nsm-barnyard2
SUBDIRS +=	nsm-daemonlogger

all:

include mk/defaults.mk
-include local.mk

mock clean:
	@for dir in $(SUBDIRS); do \
		echo "===> Making $@ in $$dir"; \
		(cd $$dir && $(MAKE) -s $@) || exit 1; \
	done

deploy:
ifndef REPO_DIR
	@echo "***> ERROR: REPO_DIR not set."
	@exit 1
else

# First try to sign all the RPMs in one one.
ifdef GPG_NAME
	@echo "===> Signing RPMs"
	@find $(SUBDIRS) -path \*/$(MOCK_RESULT)/\*.rpm -print0 | \
		xargs -0 rpmsign --resign \
		-D '_signature gpg' \
		-D '_gpg_name $(GPG_NAME)'
else
	@echo "***> WARNING: GPG_NAME not set.  Packages will not be signed."
endif

	@for dir in $(SUBDIRS); do \
		echo "===> Making $@ in $$dir"; \
		(cd $$dir && $(MAKE) deploy GPG_NAME=) || exit 1; \
	done

endif	# SKIP
