from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout
import os


class LibfooConan(ConanFile):
    name = "libfoo"
    version = "0.1.0"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libfoo here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "cmake/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        self.requires("armadillo/10.7.3")
        self.requires("date/3.0.1")

    def get_build_folder_vars_suffix(self):

        build_vars = self.conf.get(
            "layout:build_folder_vars", default=[], check_type=list
        )
        ret = []
        for s in build_vars:
            tmp = None
            if s.startswith("settings."):
                _, var = s.split("settings.", 1)
                tmp = self.settings.get_safe(var)
            elif s.startswith("options."):
                _, var = s.split("options.", 1)
                value = self.options.get_safe(var)
                if value is not None:
                    tmp = "{}_{}".format(var, value)
            else:
                raise ConanException(
                    "Invalid 'layout:build_folder_vars' value, it has"
                    " to start with 'settings.' or 'options.': {}".format(s)
                )
            if tmp:
                ret.append(tmp.lower())

        return "-".join(ret)

    def layout(self):
        gen = self.conf.get("tools.cmake.cmaketoolchain:generator", default=None)
        if gen:
            multi = "Visual" in gen or "Xcode" in gen or "Multi-Config" in gen
        else:
            compiler = self.settings.get_safe("compiler")
            if compiler in ("Visual Studio", "msvc"):
                multi = True
            else:
                multi = False

        self.folders.source = "."
        output_dir = "build"
        try:
            build_type = str(self.settings.build_type)
        except ConanException:
            raise ConanException("'build_type' setting not defined")

        if multi:
            self.folders.build = output_dir
        else:
            self.folders.build = os.path.join(
                output_dir, "cmake-build-{}".format(str(build_type).lower())
            )

        suffix = self.get_build_folder_vars_suffix()

        if suffix:
            self.folders.build += "-{}".format(suffix)

        self.folders.generators = os.path.join(
            output_dir if not suffix else os.path.join(output_dir, suffix), "generators"
        )
        self.cpp.source.includedirs = ["include"]

        if multi:
            self.cpp.build.libdirs = [f"{build_type}"]
            self.cpp.build.bindirs = [f"{build_type}"]
        else:
            self.cpp.build.libdirs = ["."]
            self.cpp.build.bindirs = ["."]

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["libfoo"]
