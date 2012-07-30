MOCK_CONFIG ?=		default

MOCK_DISTS ?=		epel-6-i386 \
			epel-6-x86_64 \
			fedora-17-i386 \
			fedora-17-x86_64

all:

-include ../local.mk

DISTFILE_DIR :=	../.cache/distfiles
RPM_CACHE :=	../.cache/rpms

RPM_NAME :=	$(shell awk '/^Name:/ { print $$2 }' $(SPEC))
RPM_VERSION =	$(shell awk '/^Version:/ { print $$2 }' $(SPEC))
RPM_RELEASE :=	$(shell awk \
		  '/^Release/ { gsub(/%{\?dist}/,".nsm"); print $$2 }' $(SPEC))

# The source RPM (SRPM) filename
SRPM_FILENAME :=$(RPM_NAME)-$(RPM_VERSION)-$(RPM_RELEASE).src.rpm

# The list of sources used by the RPM.
SOURCES :=	$(notdir $(shell spectool -l $(SPEC) | awk '{ print $$2 }'))

include ../mk/fetch.mk
include ../mk/checksum.mk
include ../mk/mock.mk

all:

local:
	@$(MAKE) fetch
	@$(MAKE) checksum
	rpmbuild \
		--define '_sourcedir $(CURDIR)/work/SOURCES' \
		--define '_specdir $(CURDIR)' \
		--define '_builddir $(CURDIR)/work/BUILD' \
		--define '_srcrpmdir $(CURDIR)/work/SRPMS' \
		--define '_rpmdir $(CURDIR)/work/RPMS' \
		--nodeps -ba $(SPEC)

work/$(SRPM_FILENAME): $(SPEC) $(addprefix SOURCES/,$(SOURCES))
	@$(MAKE) checksum
	rpmbuild \
		--define '_sourcedir $(CURDIR)/work/SOURCES' \
		--define '_specdir $(CURDIR)' \
		--define '_builddir $(CURDIR)/work/BUILD' \
		--define '_srcrpmdir $(CURDIR)/work/SRPMS' \
		--define '_rpmdir $(CURDIR)/work/RPMS' \
		--define 'dist .nsm' \
		--nodeps -bs $(SPEC)

srpm: work/$(SRPM_FILENAME)

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
ifndef REPO_ROOT
	@echo "***> ERROR: REPO_ROOT not set."
	@exit 1
endif

	@if [ ! -e "${REPO_ROOT}" ]; then \
		echo "===> Creating directory ${REPO_ROOT}"; \
		mkdir -p ${REPO_ROOT} || exit 1; \
	fi

# Make sure all packages are signed.
	@test -e reporoot && for rpm in `find reporoot -name \*.rpm`; do \
		if ! rpm --checksig $$rpm | grep -q pgp; then \
			echo "ERROR: $$rpm not signed"; \
			exit 1; \
		fi \
	done || exit 0

	test -e reporoot && find reporoot -name \*.rpm | \
		xargs python ../util/deploy.py \
		--repo-root $(REPO_ROOT) \
	 	--dist $(MOCK_DIST) --arch $(MOCK_ARCH) || exit 0

clean::
	rm -rf work reporoot

