PKGNAME=sdc-vre-check-services
SPECFILE=${PKGNAME}.spec
FILES=Makefile ${SPECFILE} vre-check-services-health.py

PKGVERSION=$(shell grep -s '^Version:' $(SPECFILE) | sed -e 's/Version:\s*//')

dist: 
        rm -rf dist
        mkdir -p dist/${PKGNAME}-${PKGVERSION}
        cp -pr ${FILES} dist/${PKGNAME}-${PKGVERSION}/.
        cd dist ; tar cfz ../${PKGNAME}-${PKGVERSION}.tar.gz ${PKGNAME}-${PKGVERSION}
        rm -rf dist

sources: dist

clean:
        rm -rf ${PKGNAME}-${PKGVERSION}.tar.gz
        rm -rf dist