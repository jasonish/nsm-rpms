SUBDIRS +=	nsm-release-el-6
SUBDIRS +=	nsm-release-fc

SUBDIRS +=	libnetfilter_queue

SUBDIRS +=	nsm-suricata1.2
SUBDIRS +=	nsm-suricata1.3
SUBDIRS +=	nsm-suricata-latest
SUBDIRS +=	nsm-suricata-select

SUBDIRS +=	nsm-libdaq
SUBDIRS +=	nsm-snort2.9.2.1
SUBDIRS +=	nsm-snort2.9.2.2
SUBDIRS +=	nsm-snort2.9.2.3
SUBDIRS +=	nsm-snort-latest
SUBDIRS +=	nsm-snort-select

SUBDIRS +=	nsm-barnyard2
SUBDIRS +=	nsm-daemonlogger

all:

-include local.mk

fetch makesum mock mock-dists clean srpm:
	@for dir in $(SUBDIRS); do \
		echo "===> Making $@ in $$dir"; \
		(cd $$dir && $(MAKE) -s $@) || exit 1; \
	done

# Global sign target.  Instead of recursing into each directory, all
# the RPMs will be signed in one go.
sign:
	@find $(SUBDIRS) -path \*reporoot/\*.rpm -print0 | \
		xargs -0 rpmsign --addsign \
		-D '_signature gpg' \
		-D '_gpg_name $(GPG_NAME)'
