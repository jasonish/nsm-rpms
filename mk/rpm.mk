MOCK_DISTS ?=		default

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
ifndef REPO_DIR
	@echo "***> ERROR: REPO_DIR not set."
	@exit 1
endif

	@if [ ! -d "${REPO_DIR}" ]; then \
		echo "***> ERROR: ${REPO_DIR} does not exist or is not a directory."; \
		exit 1; \
	fi

	@if [ ! -e "$(REPO_DIR)" ]; then \
		echo "ERROR: $(REPO_DIR) does not exist."; \
		exit 1; \
	fi

	$(MAKE) sign

	python ../util/deploy.py --repo-root $(REPO_DIR) \
	 	--dist $(MOCK_DIST) --arch $(MOCK_ARCH) \
		$(wildcard $(MOCK_RESULT)/*.rpm)

clean::
	rm -rf work reporoot

