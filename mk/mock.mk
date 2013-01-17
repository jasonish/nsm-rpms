MOCK :=		mock -r $(MOCK_CONFIG)

MOCK_DISTS ?=	epel-6-i386 \
		epel-6-x86_64 \
		fedora-17-i386 \
		fedora-17-x86_64 \
		fedora-18-i386 \
		fedora-18-x86_64

ifndef MOCK_CONFIG

# If the package specifies FOR_DISTS, filter MOCK_DISTS to only
# include those specified in FOR_DISTS.
ifdef FOR_DISTS
BUILD_DISTS := $(filter $(FOR_DISTS),$(MOCK_DISTS))
else
BUILD_DISTS := $(MOCK_DISTS)
endif

mock mock-deploy:
	@for dist in $(BUILD_DISTS); do \
		echo "Calling $(MAKE) $@ for MOCK_CONFIG=$$dist"; \
		$(MAKE) $@ MOCK_CONFIG=$$dist || exit 1; \
	done

else # MOCK_CONFIG

MOCK_DIST :=	$(shell $(MK)/get-mock-dist $(MOCK_CONFIG))
MOCK_ARCH :=	$(shell $(MK)/get-mock-arch $(MOCK_CONFIG))
MOCK_RESULT =	work/mock/$(MOCK_CONFIG)

ifdef DEPENDS
DEPENDS :=	$(shell env MOCK_DIST=$(MOCK_DIST) MOCK_ARCH=$(MOCK_ARCH) \
			$(MK)/resolve-deps $(DEPENDS))
DEPENDS :=	$(addprefix $(RPM_CACHE)/,$(DEPENDS))
endif

# Use mock to build the package.
mock: work/SRPMS/$(SRPM)

	rm -rf $(MOCK_RESULT)

	$(MOCK) --init

ifdef DEPENDS
	@for dep in $(DEPENDS); do \
	    if [ ! -e $$dep ]; then \
		echo "***> ERROR: Dependency package $$dep does not exist."; \
		exit 1; \
	    else \
		echo "===> Found dependency $$dep."; \
	    fi \
	done
	$(MOCK) $(foreach path, $(DEPENDS), --install $(path))
endif

	$(MOCK) -v --no-cleanup-after --no-clean \
		--resultdir=$(MOCK_RESULT) \
		$(RPM_MACROS) \
		work/SRPMS/$(SRPM)
	$(MOCK) clean
	mkdir -p $(RPM_CACHE)

# Caches the RPM for use by other builds inside mock.
	cp $(MOCK_RESULT)/*.rpm $(RPM_CACHE)

	$(MAKE) mock-deploy

# Copies the resulting RPMs into a yum repo style directory tree.
mock-deploy:
	mkdir -p ./reporoot
	find $(MOCK_RESULT) -name \*.rpm | \
		xargs $(MK)/deploy --root ./reporoot

endif # MOCK_CONFIG
