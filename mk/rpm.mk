TOPDIR :=	$(realpath $(dir $(word 2,$(MAKEFILE_LIST)))..)
export TOPDIR
MK :=		$(TOPDIR)/mk

DISTFILE_DIR :=	$(TOPDIR)/cache/distfiles
RPM_CACHE :=	$(TOPDIR)/cache/rpms

RPM_NAME :=	$(shell awk '/^Name:/ { print $$2 }' $(SPEC))
RPM_VERSION =	$(shell awk '/^Version:/ { print $$2 }' $(SPEC))
RPM_RELEASE :=	$(shell awk \
		  '/^Release/ { gsub(/%{\?dist}/,""); print $$2 }' $(SPEC))

# The source RPM (SRPM) filename
SRPM_FILENAME :=$(RPM_NAME)-$(RPM_VERSION)-$(RPM_RELEASE).nsm.src.rpm

# The list of sources used by the RPM.
SOURCES :=	$(notdir $(shell spectool -l $(SPEC) | awk '{ print $$2 }'))

RPM_MACROS :=	--define 'nsm_prefix /opt/nsm'
RPM_MACROS +=	--define '_defaultdocdir /opt/nsm/share/doc'

all:
	@echo ""
	@echo "usage:"
	@echo ""
	@echo "  $(MAKE) mock     Build in mock for all distributions"
	@echo "  $(MAKE) local    Build for local system"
	@echo "  $(MAKE) srpms    Build SRPM"
	@echo "  $(MAKE) sign     Sign built RPMs."
	@echo ""

-include $(TOPDIR)/local.mk
include $(MK)/fetch.mk
include $(MK)/checksum.mk
include $(MK)/mock.mk

local:
	@$(MAKE) fetch
	@$(MAKE) checksum
	echo $(RPM_MACROS)
	rpmbuild \
		--define '_sourcedir $(CURDIR)/work/SOURCES' \
		--define '_specdir $(CURDIR)' \
		--define '_builddir $(CURDIR)/work/BUILD' \
		--define '_srcrpmdir $(CURDIR)/work/SRPMS' \
		--define '_rpmdir $(CURDIR)/work/RPMS' \
		$(RPM_MACROS) \
		-ba $(SPEC)

work/SRPMS/$(SRPM_FILENAME): $(SPEC) $(addprefix work/SOURCES/,$(SOURCES))
	@$(MAKE) checksum
	rpmbuild \
		--define '_sourcedir $(CURDIR)/work/SOURCES' \
		--define '_specdir $(CURDIR)' \
		--define '_builddir $(CURDIR)/work/BUILD' \
		--define '_srcrpmdir $(CURDIR)/work/SRPMS' \
		--define '_rpmdir $(CURDIR)/work/RPMS' \
		--define 'dist .nsm' \
		--nodeps -bs $(SPEC)
	@echo $^

srpm: work/SRPMS/$(SRPM_FILENAME)

sign:
ifndef GPG_NAME
	@echo "***> ERROR: Not signing. GPG_NAME not set."
	@exit 1
else
	find reporoot -name \*.rpm | xargs rpmsign --addsign \
		-D '_signature gpg' \
		-D '_gpg_name $(GPG_NAME)'
endif

deploy:
# Make sure all packages are signed.
	@test -e reporoot && for rpm in `find reporoot -name \*.rpm`; do \
		if ! rpm --checksig $$rpm | grep -q pgp; then \
			echo "ERROR: $$rpm not signed"; \
			exit 1; \
		fi \
	done || exit 0

ifdef DEPLOY_COMMAND
	test -e reporoot && $(DEPLOY_COMMAND) || exit 0
else
	@echo "No DEPLOY_COMMAND specified.  Nothing to do."
endif

clean::
	rm -rf work reporoot
	find . -name \*~ | xargs rm -f
