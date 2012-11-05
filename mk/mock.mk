MOCK :=		mock -r $(MOCK_CONFIG)

MOCK_DISTS ?=	epel-6-i386 \
		epel-6-x86_64 \
		fedora-17-i386 \
		fedora-17-x86_64

ifndef MOCK_CONFIG

# If the package specifies FOR_DISTS, filter MOCK_DISTS to only
# include those specified in FOR_DISTS.
ifdef FOR_DISTS
MOCK_DISTS := $(filter $(FOR_DISTS),$(MOCK_DISTS))
endif

mock:
	@for dist in $(MOCK_DISTS); do \
		$(MAKE) mock MOCK_CONFIG=$$dist || exit 1; \
	done

else # MOCK_CONFIG

MOCK_DIST :=	$(shell python -c 'config_opts = {}; \
			exec(open("/etc/mock/$(MOCK_CONFIG).cfg").read()); \
			print config_opts["dist"]')
MOCK_ARCH :=	$(shell python -c 'config_opts = {}; \
			exec(open("/etc/mock/$(MOCK_CONFIG).cfg").read()); \
			print config_opts["target_arch"]')
MOCK_RESULT =	work/mock/$(MOCK_CONFIG)

MOCK_INSTALL :=	$(addprefix $(RPM_CACHE)/,\
	$(addsuffix .$(MOCK_DIST).$(MOCK_ARCH).rpm,$(MOCK_INSTALL)))

# Use mock to build the package.
mock: work/SRPMS/$(SRPM_FILENAME)

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

endif # MOCK_CONFIG
