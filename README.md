# Android Platform Tools

Android Platform Tools for Android. This is based on [android-sdk-tools](https://github.com/lzhiyong/android-sdk-tools) by @lzhiyong.

# Building

Follow the steps below to build the tools.

## Before we start

You need `Android NDK r26` in order to build this project. Earlier versions may not work.

## Get the source

Use the `get_source.py` Python script to fetch the sources for required repositories :

```bash
python get_source.py --tag=platform-tools-34.0.0
```

Please note that the `get_source.py` script clones only the specified tag to avoid cloning the entire repository. The cloned repositories are in a `DETACHED HEAD` state. This is enough for 'just building the tools'. However, in some cases, you might want to clone the entire repositories which can be done by editing the `get_source.py` script (you can prefer @lzhiyong's repo in this case which uses git submodules).

## Apply the patches

Most of the patches that are available in the `patches` directory should be compatible with `git apply`. You could run `git apply patches/<filename>.patch` for every `.patch` file to patch the source. If any of the patches fail, you'll have to manually apply the patches.

> NOTE : Prefer applying the patches one by one over applying all of them at once.

## Build protoc

We need to build `protobuf` for the host OS which will be used to generate the required sources. To do this, `cd` into protobuf directory :
```bash
cd src/protobuf
```

Create a symlink to the `googletest` directory :
```bash
# Skip this if you do not want to build tests
ln -sf $(realpath ../googletest) third_party/googletest
```

Execute `cmake` to generate the build files :
```bash
cmake -GNinja

# or if you want to skip tests
cmake -GNinja -Dprotobuf_BUILD_TESTS=OFF
```

Start building `protoc` with :
```bash
ninja -j$(nproc --all)
```

Once the build process succeeds, you should have the `protoc` executable in your working directory.

## Setup boringssl

We need to create a symlink in the `src/boringssl/src/third_party` directory which should point to the `googletest` directory. To do this, execute the following command from THIS project's root directory :

```bash
ln -sf $(realpath ./src/googletest/googletest) ./src/boringssl/src/third_party/googletest
```

## Start the build

Use the `build.py` script to build the tools :
```bash
# To build for aarch64
# Generated executables will be located in build/aarch64/bin
python build.py \
    --ndk=/path/to/android-ndk-r26 \
    --api=30 \
    --abi=arm64-v8a \
    --protoc=$PWD/src/protobuf/protoc \
    --build=build/aarch64

# To build for arm
# Generated executables will be located in build/arm/bin
python build.py \
    --ndk=/path/to/android-ndk-r26 \
    --api=30 \
    --abi=armeabi-v7a \
    --protoc=$PWD/src/protobuf/protoc \
    --build=build/arm
```