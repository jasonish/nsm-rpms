SUBDIRS +=	nsm-release-el-6
SUBDIRS +=	nsm-release-fc

# Libraries.
SUBDIRS +=	libnetfilter_queue
SUBDIRS +=	jansson
SUBDIRS +=	libdaq

# Suricata.
SUBDIRS +=	suricata1.3.5
SUBDIRS +=	suricata1.4
SUBDIRS +=	suricata-latest
SUBDIRS +=	suricata-select

# Snort.
SUBDIRS +=	snort2.9.2.3
SUBDIRS +=	snort2.9.3
SUBDIRS +=	snort2.9.3.1
SUBDIRS +=	snort2.9.4
SUBDIRS +=	snort-latest
SUBDIRS +=	snort-select

# Other tools.
SUBDIRS +=	barnyard2
SUBDIRS +=	daemonlogger
SUBDIRS +=	netsniff-ng
SUBDIRS +=	pulledpork

all:

-include local.mk

fetch makesum mock mock-dists clean srpm deploy deploy-dists::
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

clean::
	find . -name \*~ -exec rm -f {} \;
