include ../mk/defaults.mk

all:

-include ../local.mk

NAME =		$(shell awk '/^Name:/ { print $$2 }' $(SPEC))
VERSION =	$(shell awk '/^Version:/ { print $$2 }' $(SPEC))

RELEASE :=	$(shell awk \
		  '/^Release/ { gsub(/%{\?dist}/,".nsm"); print $$2 }' $(SPEC))
SRPM :=		$(NAME)-$(VERSION)-$(RELEASE).src.rpm

SOURCES =	$(shell spectool -l $(SPEC) | awk '{ print $$2 }')
FILES :=	$(notdir $(SOURCES))

# Those sources that are remote (ie: have a URL).
REMOTE_SRCS =	$(filter http:%,$(SOURCES))
REMOTE_FILES =	$(notdir $(REMOTE_SRCS))

SRC_CACHE :=	../.cache/distfiles
RPM_CACHE :=	../.cache/rpms

MOCK_DIST :=	$(shell python -c 'config_opts = {}; \
			exec(open("/etc/mock/$(MOCK_CONFIG).cfg").read()); \
			print config_opts["dist"]')
MOCK_ARCH :=	$(shell python -c 'config_opts = {}; \
			exec(open("/etc/mock/$(MOCK_CONFIG).cfg").read()); \
			print config_opts["target_arch"]')

MOCK_RESULT =	work/mock/$(MOCK_CONFIG)

MOCK :=		mock -r $(MOCK_CONFIG)

# Some packages may only be for certain distributions.  If FOR_DISTS is defined
# and the MOCK_CONFIG is not included in the FOR_DISTS set SKIP.
ifdef FOR_DISTS
ifneq ($(filter $(FOR_DISTS),$(MOCK_CONFIG)),$(MOCK_CONFIG))
SKIP = yes
endif
endif

ifdef SKIP

mock local deploy:
	@echo "***> Package not supported for distribution $(MOCK_CONFIG)"

else	# SKIP

all:

info:
	@echo "MOCK_DIST: $(MOCK_DIST)"
	@echo "MOCK_ARCH: $(MOCK_ARCH)"
	@echo "MOCK_RESULT: $(MOCK_RESULT)"

# Use spectool to download all sources/patches with a URL.  But before
# downloading first check our local cache.
$(REMOTE_FILES):
	@if [ -e $(SRC_CACHE)/$@ ]; then \
		echo "===> Copying $@ from cache"; \
		cp $(SRC_CACHE)/$@ . ; \
	else \
		echo "===> Fetching sources"; \
		spectool -g $(SPEC); \
		mkdir -p $(SRC_CACHE); \
		cp $(notdir $(REMOTE_SRCS)) $(SRC_CACHE); \
	fi

# fetch: an alias to download the files.
fetch: $(REMOTE_FILES)

# Use mock to build the package.  Mock depends on the SRPM.
mock: MOCK_INSTALL := $(addsuffix .$(MOCK_DIST).$(MOCK_ARCH).rpm,\
			$(MOCK_INSTALL))
mock: MOCK_INSTALL := $(addprefix $(RPM_CACHE)/,$(MOCK_INSTALL))
mock: work/$(SRPM)

	rm -rf $(MOCK_RESULT)

	$(MOCK) --init

ifdef MOCK_INSTALL
	@for filename in $(MOCK_INSTALL); do \
		if [ ! -e $$filename ]; then \
		    echo "***> ERROR: $$filename does not exist in the cache"; \
		    exit 1; \
		fi \
	done
	$(MOCK) --install $(foreach path, $(MOCK_INSTALL), --install $(path))
endif
	$(MOCK) -v --no-cleanup-after --no-clean \
		--resultdir=$(MOCK_RESULT) work/$(SRPM)
	$(MOCK) clean
	mkdir -p $(RPM_CACHE)
	cp $(MOCK_RESULT)/*.rpm $(RPM_CACHE)

local: $(FILES) checksum
	rpmbuild \
		--define '_sourcedir $(CURDIR)' \
		--define '_specdir $(CURDIR)' \
		--define '_builddir $(CURDIR)/BUILD' \
		--define '_srcrpmdir $(CURDIR)/SRPMS' \
		--define '_rpmdir $(CURDIR)/RPMS' \
		--nodeps -ba $(SPEC)

work/$(SRPM): $(SPEC) $(FILES)
	rpmbuild \
		--define '_sourcedir .' \
		--define '_specdir .' \
		--define '_builddir .' \
		--define '_srcrpmdir work' \
		--define '_rpmdir .' \
		--define 'dist .nsm' \
		--nodeps -bs $(SPEC)

srpm: work/$(SRPM)

makesum:
ifdef FILES
	@echo "===> Writing sources"
	@md5sum $(FILES) > sources
endif

checksum:
ifdef FILES
	@echo "===> Verifying checksums"
	@if [ ! -e sources ]; then \
	    echo "***> ERROR sources file does not exist. Run: make makesum"; \
	    exit 1; \
	fi
	@md5sum -c sources
endif

clean::
	rm -rf BUILD RPMS SRPMS
	rm -rf work
	rm -f $(notdir $(REMOTE_SRCS))

sign:
ifndef GPG_NAME
	@echo "***> ERROR: Not signing. GPG_NAME not set."
	@exit 1
else
	rpmsign --addsign \
		-D '_signature gpg' \
		-D '_gpg_name $(GPG_NAME)' \
		$(wildcard $(MOCK_RESULT)/*.rpm)
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

endif	# SKIP

# Like deploy, but deploys into the local directory.
deploy-local:
ifdef GPG_NAME
	@$(MAKE) sign
endif
	@mkdir -p $(LOCAL_DEPLOY_DIR)
	python ../util/deploy.py --repo-root $(LOCAL_DEPLOY_DIR) \
		--dist $(MOCK_DIST) --arch $(MOCK_ARCH) \
		$(wildcard $(MOCK_RESULT)/*.rpm)
