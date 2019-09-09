from cpt.packager import ConanMultiPackager
from conans import tools


if __name__ == "__main__":
    builder = ConanMultiPackager(
        username = "ledocc",
        reference = "libvncserver/"+tools.load("version.txt"),
        channel = "testing",
        stable_branch_pattern = "release/*"
    )
    builder.add_common_builds()
    builder.run()
