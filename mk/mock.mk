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

mock mock-deploy:
	@for dist in $(MOCK_DISTS); do \
		$(MAKE) $@ MOCK_CONFIG=$$dist || exit 1; \
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

	$(MAKE) mock-deploy

ifeq ($(MOCK_DIST),el6)
REPO_PREFIX := reporoot/el/6/
else ifeq ($(MOCK_DIST),fc17)
REPO_PREFIX := reporoot/fedora/17
endif
REPO_ARCH := $(subst i686,i386,$(MOCK_ARCH))
mock-deploy:
	mkdir -p $(REPO_PREFIX)/SRPMS
	mkdir -p $(REPO_PREFIX)/$(REPO_ARCH)
	mkdir -p $(REPO_PREFIX)/$(REPO_ARCH)/debug
	cp $(MOCK_RESULT)/*.$(MOCK_DIST).$(MOCK_ARCH).rpm \
		$(REPO_PREFIX)/$(REPO_ARCH)
	-mv $(REPO_PREFIX)/$(REPO_ARCH)/*debuginfo*.rpm \
		$(REPO_PREFIX)/$(REPO_ARCH)/debug
	cp $(MOCK_RESULT)/*.$(MOCK_DIST).src.rpm $(REPO_PREFIX)/SRPMS

endif # MOCK_CONFIG
