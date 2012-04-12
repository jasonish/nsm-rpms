SPEC =		nsm-barnyard2.spec

SOURCE_FILE =	barnyard2-1.10.tar.gz
SOURCE_URL =	https://github.com/firnsy/barnyard2/tarball/v2-1.10-beta2

include ../mk/rpm.mk

$(SOURCE_FILE):
	if [ -e $(SRC_CACHE)/$@ ]; then \
		cp $(SRC_CACHE)/$@ .; \
	else \
		wget -O $@ $(SOURCE_URL); \
		cp $@ $(SRC_CACHE); \
	fi

clean::
	rm -f $(SOURCE_FILE)

