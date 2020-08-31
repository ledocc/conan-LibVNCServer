from conans import ConanFile, CMake, tools
import os

class LibvncserverConan(ConanFile):
    name = "libvncserver"
    version = tools.load("version.txt").rstrip()
    license = "GPL 2.0"
    author = "David Callu - callu.david at gmail.com"
    url = "https://github.com/ledocc/conan-libvncserver"
    description = "A library for easy implementation of a VNC server"
    topics = ("vnc" "vnc-client" "vnc-server" "library" "remote-desktop")
    settings = "os", "compiler", "build_type", "arch"
    options = dict({
        "shared": [True, False],
        "fPIC": [True, False],
        "with_24bpp": [True, False],
#        "with_gcrypt": [True, False],
#        "with_gnutls": [True, False],
        "with_ipv6": [True, False],
        "with_jpeg": [True, False],
#        "with_lzo": [True, False],
        "with_openssl": [True, False],
        "with_png": [True, False],
#        "with_sasl": [True, False],
#        "with_systemd": [True, False],
        "with_threads": [True, False],
        "with_websockets": [True, False],
        "with_zlib": [True, False]
    })

    default_options = dict({
        "shared": False,
        "fPIC": True,
        "with_24bpp": True,
#        "with_gcrypt": False,
#        "with_gnutls": False,
        "with_ipv6": True,
        "with_jpeg": True,
#        "with_lzo": False,
        "with_openssl": True,
        "with_png": True,
#        "with_sasl": False,
#        "with_systemd": False,
        "with_threads": True,
        "with_websockets": True,
        "with_zlib": True
    })

    generators = ["cmake", "cmake_paths"]
    homepage = "https://github.com/LibVNC/libvncserver"
    build_requires = (("cmake/3.18.0@"),
                      ("ninja/1.9.0@" ))

    exports_sources = ['patches/*', 'conan_requirement.cmake']
    exports = ['version.txt']

    folder_name = "libvncserver-LibVNCServer-{}".format( version )


    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        archive_name = "LibVNCServer-"+self.version+".tar.gz"
        tools.get( self.homepage+"/archive/"+archive_name,
                   sha256="33cbbb4e15bb390f723c311b323cef4a43bcf781984f92d92adda3243a116136")

        tools.patch(patch_file="patches/cmake_export.patch",
                        base_path=os.path.join(self.source_folder, self.folder_name))


    def requirements(self):
#        if self.options.with_gcrypt:
#            self.requires("")
#        if self.options.with_gnutls:
#            self.requires("")
        if self.options.with_jpeg:
            self.requires("libjpeg-turbo/2.0.5")
#        if self.options.with_lzo:
#            self.requires("")
        if self.options.with_openssl:
            self.requires("openssl/1.1.1g")
        if self.options.with_png:
            self.requires("libpng/1.6.37")
#        if self.options.with_sasl:
#            self.requires("")
#        if self.options.with_systemd:
#            self.requires("")
        if self.options.with_zlib:
            self.requires("zlib/1.2.11")


    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        if self._should_build_test() and self._should_run_test():
            self.run("ctest --output_on_failure --timeout=3000", cwd=cmake.build_folder)

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("COPYING", dst="licenses/LibVNCServer", ignore_case=True)


    def _configure_cmake(self):
        cmake = CMake(self, set_cmake_flags=True)
        cmake.generator="Ninja"
        cmake.verbose=True
        self.output.info( "self.build_folder = {}".format( self.build_folder, ) )
        cmake.definitions["CMAKE_PROJECT_INCLUDE"] = os.path.join( self.build_folder, "conan_requirement.cmake")

        if not self._should_build_test():
            cmake.definitions["BUILD_TESTING"]="OFF"

        cmake.definitions["WITH_24BPP"] = "ON" if self.options.with_24bpp else "OFF"
        cmake.definitions["WITH_FFMPEG"] = "OFF"
        cmake.definitions["WITH_GCRYPT"] = "OFF" #"ON" if self.options.with_gcrypt else "OFF"
        cmake.definitions["WITH_GNUTLS"] = "OFF" #"ON" if self.options.with_gnutls else "OFF"
        cmake.definitions["WITH_IPV6"] = "ON" if self.options.with_ipv6 else "OFF"
        cmake.definitions["WITH_JPEG"] = "ON" if self.options.with_jpeg else "OFF"
        cmake.definitions["WITH_LZO"] = "OFF" #"ON" if self.options.with_lzo else "OFF"
        cmake.definitions["WITH_OPENSSL"] = "ON" if self.options.with_openssl else "OFF"
        cmake.definitions["WITH_PNG"] = "ON" if self.options.with_png else "OFF"
        cmake.definitions["WITH_SASL"] = "OFF" #"ON" if self.options.with_sasl else "OFF"
        cmake.definitions["WITH_SDL"] = "OFF"
        cmake.definitions["WITH_SYSTEMD"] = "OFF" #"ON" if self.options.with_systemd else "OFF"
        cmake.definitions["WITH_THREADS"] = "ON" if self.options.with_threads else "OFF"
        cmake.definitions["WITH_TIGHTVNC_FILETRANSFER"] = "OFF"
        cmake.definitions["WITH_WEBSOCKETS"] = "ON" if self.options.with_websockets else "OFF"
        cmake.definitions["WITH_ZLIB"] = "ON" if self.options.with_zlib else "OFF"



        cmake.configure(source_dir=self.folder_name)
        return cmake

    def _should_build_test(self):
        if ( self.settings.get_safe("compiler") == "Visual Studio" ) and ( self.settings.get_safe("build_type") == "Debug" ) :
            self.output.warn("Skipping test : Visual Studio build in Debug mode fail to compile.")
            return False
        return True

    def _should_run_test(self):
        if tools.cross_building(self.settings):
            self.output.warn("Skipping test : cross built package.")
            return False
        return True
