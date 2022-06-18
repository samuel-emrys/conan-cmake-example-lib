# libfoo

## Install dependencies

```bash
$ conan install . --build=missing
```

## Build the project

Any of the following methods will work:

```bash
$ conan build .
```

```bash
$ cmake --preset Release
$ cmake --build --preset Release
```

```bash
$ cmake . -DCMAKE_TOOLCHAIN_FILE=build/generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release -B build/cmake-build-release
$ cmake --build build/cmake-build-release
```

## Create the library

```bash
$ conan create .
```
