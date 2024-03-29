#!/usr/bin/env python3
#
# Copyright © 2022 Github Lzhiyong
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# pylint: disable=not-callable, line-too-long, no-else-return

import os
import time
import shutil
import argparse
import subprocess
from pathlib import Path

supported_abis = ["armeabi-v7a", "arm64-v8a", "x86", "x86_64"]

def check_abi_supported(abi: str):
    if not abi in supported_abis :
        raise ValueError(f"ABI {abi} is not supported!")

def format_time(seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    
    hour = int(hour)
    minute = int(minute)
    if minute < 1:
        sec = float('%.2f' % sec)
    else:
        sec = int(sec)

    if hour != 0:
        return "{}h{}m{}s".format(hour, minute, sec)
    elif minute != 0:
        return "{}m{}s".format(minute, sec)
    else:
        return "{}s".format(sec)

def finish(args, build_dir):
    cwd = Path(os.getcwd())
    strip = args.ndk + "/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-strip"

    build_tools_dir = cwd / "{}/bin/build-tools".format(build_dir)
    if not build_tools_dir.exists():
        build_tools_dir.mkdir()

    platform_tools_dir = cwd / "{}/bin/platform-tools".format(build_dir)
    if not platform_tools_dir.exists():
        platform_tools_dir.mkdir()

    build_tools = ['aapt', 'aapt2', 'aidl', 'zipalign', 'dexdump', 'split-select']
    for tool in build_tools:
        if Path(build_tools_dir.parent / tool).exists():
            shutil.copy2(build_tools_dir.parent / tool, build_tools_dir)
            os.remove(build_tools_dir.parent / tool)
            subprocess.run("{} -g {}".format(strip, build_tools_dir / tool), shell=True)

    platform_tools = [
        'adb', 'fastboot', 'sqlite3', 'dmtracedump', 'etc1tool', 'hprof-conv',
        'e2fsdroid', 'sload_f2fs', 'mke2fs', 'make_f2fs', 'make_f2fs_casefold'
    ]
    for tool in platform_tools:
        if Path(platform_tools_dir.parent / tool).exists():
            shutil.copy2(platform_tools_dir.parent / tool, platform_tools_dir)
            os.remove(build_tools_dir.parent / tool)
            subprocess.run("{} -g {}".format(strip, platform_tools_dir / tool), shell=True)


def build(args):

    abis: str = args.abi

    if ',' in abis:

        # Fail early, in case of unsupported ABIs
        for abi in abis.split(','):
            check_abi_supported(abi.strip())

        # Build for each ABI
        for abi in abis.split(','):
            buildFor(abi.strip(), args)

        return
    
    buildFor(abis.strip(), args)

def buildFor(abi: str, args):
    
    print(f"Building for ABI: {abi}...")

    ndk = Path(args.ndk)
    cmake_toolchain_file = ndk / "build/cmake/android.toolchain.cmake"
    if not cmake_toolchain_file.exists():
        raise ValueError("no such file or directory: {}".format(cmake_toolchain_file))

    build_dir = f"{args.build}/android{args.api}-{abi}"
    command = [args.cmake, "-GNinja", 
        "-B {}".format(build_dir),
        "-DANDROID_NDK={}".format(args.ndk),
        "-DCMAKE_TOOLCHAIN_FILE={}".format(cmake_toolchain_file),
        "-DANDROID_PLATFORM=android-{}".format(args.api),
        "-DCMAKE_ANDROID_ARCH_ABI={}".format(abi),
        "-DANDROID_ABI={}".format(abi),
        "-DCMAKE_SYSTEM_NAME=Android",
        "-Dprotobuf_BUILD_TESTS=OFF",
        "-DABSL_PROPAGATE_CXX_STD=ON",
        "-DANDROID_ARM_NEON=ON",
        "-DCMAKE_BUILD_TYPE=Release"]

    if not Path(build_dir).exists():
        print(f"'{build_dir}' does not exist! Creating directory...")
        os.makedirs(build_dir)
    
    if args.protoc is not None:
        if not Path(args.protoc).exists():
            raise ValueError("no such file or directory: {}".format(args.protoc))
        command.append("-DPROTOC_PATH={}".format(args.protoc))
    
    result = subprocess.run(command)
    start = time.time()
    if result.returncode == 0:
        if args.target == "all":
            result = subprocess.run(["ninja", "-C", build_dir, "-j {}".format(args.job)])
        else:
            result = subprocess.run(["ninja", "-C", build_dir, args.target, "-j {}".format(args.job)])

    if result.returncode == 0:
        # build finish
        finish(args, build_dir)
        end = time.time()
        print("\033[1;32mbuild success cost time: {}\033[0m".format(format_time(end - start)))

    
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--ndk", required=True, help="Set the NDK toolchain path.")
    parser.add_argument("--abi", required=True, help="Comma separated list of CPU ABIs to build for.")
    parser.add_argument("--api", default=30, help="Set android platform level, minimum API is 30.")
    parser.add_argument('--build', default='build', help='Set the build directory.')
    parser.add_argument("--job", default=16, help="Run N jobs in parallel, default is 16.")
    parser.add_argument("--target", default="all", help="Build specified targets such as aapt2, adb, fastboot, etc.")
    parser.add_argument("--protoc", help="Set the host protoc (protobuf compiler) path.")
    parser.add_argument("--cmake", default="cmake", help="Set the host `cmake` binary path.")
    
    args = parser.parse_args()

    build(args)

if __name__ == "__main__":
    main()
