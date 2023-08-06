import fnmatch
import os
import subprocess

from lektor.pluginsystem import Plugin
from lektor.reporter import reporter
from lektor.utils import portable_popen


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


class CSSBuildPlugin(Plugin):
    name = "lektor-cssbuild"
    description = "A Lektor plugin for building CSS assets"

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        self.options = self.get_config()

    def is_enabled(self, builder):
        extra_flags = getattr(builder, "extra_flags", getattr(builder, "build_flags", None))
        return bool(extra_flags.get("cssbuild"))

    def npm_install(self):
        reporter.report_generic("Running npm install")
        npm_root = os.path.join(self.env.root_path, ".")
        portable_popen(["npm", "install"], cwd=npm_root).wait()

    def run_sass(self, source, output):
        npm_root = os.path.join(self.env.root_path, ".")
        args = [
            os.path.join(npm_root, "node_modules", ".bin", "node-sass"),
            source,
            "-o",
            output,
        ]
        portable_popen(args, cwd=npm_root).wait()

    def run_uncss(self, sources, output):
        npm_root = os.path.join(self.env.root_path, ".")
        args = [os.path.join(npm_root, "node_modules", ".bin", "uncss")]
        args.extend(sources)
        args.append("-n")
        args.append("-o")
        args.append(output)
        ignore = self.options.get("uncss.ignore", "")
        if len(ignore) > 0:
            args.append("-i")
            args.append(ignore)
        portable_popen(args, cwd=npm_root).wait()

    def run_cssmin(self, source, output):
        npm_root = os.path.join(self.env.root_path, ".")
        args = [os.path.join(npm_root, "node_modules", ".bin", "cssmin"), source]
        out, err = portable_popen(args, cwd=npm_root, stdout=subprocess.PIPE).communicate()
        with open(output, "wb") as f:
            f.write(out)

    def get_option_path(self, option, builder):
        option_value = self.options.get(option)
        prefix, path = option_value.split(":")
        root_path = self.env.root_path if prefix != "dst" else builder.destination_path
        return os.path.join(root_path, path)

    def on_before_build_all(self, builder, **extra):
        if not self.is_enabled(builder):
            return

        if len(self.options) > 0:
            self.npm_install()

        if "sass" in self.options.sections():
            reporter.report_generic("Starting node-sass")
            source = self.get_option_path("sass.source", builder)
            output = self.get_option_path("sass.output", builder)
            self.run_sass(source, output)
            reporter.report_generic("Finished node-sass")

    def on_after_build_all(self, builder, **extra):
        if not self.is_enabled(builder):
            return

        if "uncss" in self.options.sections():
            reporter.report_generic("Starting uncss")
            asset_dirs = tuple(
                os.path.join(builder.destination_path, d)
                for d in os.listdir(self.env.asset_path)
            )
            sources = [
                f
                for f in find_files(builder.destination_path, "*.html")
                if not f.startswith(asset_dirs)
            ]
            output = self.get_option_path("uncss.output", builder)
            self.run_uncss(sources, output)
            reporter.report_generic("Finished uncss")

        if "cssmin" in self.options.sections():
            reporter.report_generic("Starting cssmin")
            source = self.get_option_path("cssmin.source", builder)
            output = self.get_option_path("cssmin.output", builder)
            self.run_cssmin(source, output)
            reporter.report_generic("Finished cssmin")
