# Android Platform Tools


# Building

First of all, we need to build protobuf for the host OS. To do this, `cd` into protobuf directory :
```bash
cd src/protobuf
```

Create a symlink to the `googletest` directory :
```bash
# Skip this if you do not want to build tests
ln -sf $(realpath ../googletest) third_party/googletest
```

Execute `cmake` to generate the build files :
``` bash
cmake -GNinja

# or to skip tests
cmake -GNinja -Dprotobuf_BUILD_TESTS=OFF
```

Start building `protoc` with :
```
ninja -j$(nproc --all)
```

Once the build process succeeds, you should have the `protoc` executable in your working directory.