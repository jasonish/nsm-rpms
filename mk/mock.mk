MOCK :=		mock -r $(MOCK_CONFIG)

ifdef MOCK_CONFIG
MOCK_DIST :=	$(shell python -c 'config_opts = {}; \
			exec(open("/etc/mock/$(MOCK_CONFIG).cfg").read()); \
			print config_opts["dist"]')
MOCK_ARCH :=	$(shell python -c 'config_opts = {}; \
			exec(open("/etc/mock/$(MOCK_CONFIG).cfg").read()); \
			print config_opts["target_arch"]')
MOCK_RESULT =	work/mock/$(MOCK_CONFIG)

MOCK_INSTALL :=	$(addprefix $(RPM_CACHE)/,\
	$(addsuffix .$(MOCK_DIST).$(MOCK_ARCH).rpm,$(MOCK_INSTALL)))
endif

# Some packages may only be for certain distributions.  If FOR_DISTS is defined
# and the MOCK_CONFIG is not included in the FOR_DISTS set NO_BUILD
ifdef FOR_DISTS
ifneq ($(filter $(FOR_DISTS),$(MOCK_CONFIG)),$(MOCK_CONFIG))
NO_BUILD = yes
endif
endif

ifeq ($(NO_BUILD),yes)

mock mock-deploy:
	@echo This package is not supported for this mock configuration.

else

# Use mock to build the package.
mock: work/$(SRPM_FILENAME)

ifndef MOCK_CONFIG
	@echo "No MOCK_CONFIG specified."
	@exit 1
endif

	rm -rf $(MOCK_RESULT)

	$(MOCK) --init

ifdef MOCK_INSTALL
	@for filename in $(MOCK_INSTALL); do \
		if [ ! -e $$filename ]; then \
		    echo "***> ERROR: $$filename does not exist in the cache"; \
		    exit 1; \
		fi \
	done
	$(MOCK) $(foreach path, $(MOCK_INSTALL), --install $(path))
endif

	$(MAKE) srpm
	$(MOCK) -v --no-cleanup-after --no-clean \
		--resultdir=$(MOCK_RESULT) work/SRPMS/$(SRPM_FILENAME)
	$(MOCK) clean
	mkdir -p $(RPM_CACHE)

# Caches the RPM for use by other builds inside mock.
	cp $(MOCK_RESULT)/*.rpm $(RPM_CACHE)

# Deploy locally into the projects directory in a yum repo style
# directory tree.
	@mkdir -p reporoot
	@python ../util/deploy.py --repo-root reporoot \
		--dist $(MOCK_DIST) --arch $(MOCK_ARCH) \
		$(MOCK_RESULT)/*.rpm

endif # NO_BUILD

mock-dists:
	@for dist in $(MOCK_DISTS); do \
		$(MAKE) mock MOCK_CONFIG=$$dist; \
	done
