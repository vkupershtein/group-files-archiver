#!/bin/bash
set -euo pipefail

PKG_NAME="group-files-archiver"
PKG_VERSION="0.1.0"
SRC_DIR="${PKG_NAME}-${PKG_VERSION}"

# Clean old builds
rm -rf ../${SRC_DIR} ../${PKG_NAME}_*.deb ../${PKG_NAME}_*.orig.tar.gz

# Step 1: Prepare source dir with correct Debian naming
cp -r . ../${SRC_DIR}
cd ../${SRC_DIR}

# Step 2: Create tarball
tar --exclude=debian -czf ../${PKG_NAME}_${PKG_VERSION}.orig.tar.gz .

# Step 3: Install required packaging tools
sudo apt-get update
sudo apt-get install -y build-essential devscripts debhelper python3-all python3-setuptools

# Step 4: Build package
debuild -us -uc

echo "Build complete."
