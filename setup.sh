#!/bin/bash

# Build protoc for host OS
cd src/protobuf
cmake -GNinja -Dprotobuf_BUILD_TESTS=OFF
ninja -j$(nproc --all)

# Symlink googletest in boringssl
ln -sf $(realpath ./src/googletest/googletest) ./src/boringssl/src/third_party/googletest