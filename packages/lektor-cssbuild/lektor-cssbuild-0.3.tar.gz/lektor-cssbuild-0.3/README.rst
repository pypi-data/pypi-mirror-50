|pypi|

.. |pypi| image:: https://img.shields.io/pypi/v/lektor-cssbuild.svg?style=flat-square
    :target: https://pypi.org/project/lektor-cssbuild/
    :alt: PyPI version.

lektor-cssbuild is a plugin for the `Lektor <https://www.getlektor.com>`_
static site generator that integrates CSS manipulation tools
into the build process. The tools that it uses are:

- `libsass-python <https://github.com/sass/libsass-python>`_ is run
  before the Lektor build to generate a CSS file.

- `uncss <https://github.com/uncss/uncss>`_ is run
  after the Lektor build to remove unused CSS.

- `rcssmin <https://github.com/ndparker/rcssmin/>`_ is run
  as the last step to minify the CSS.

To use the plugin, add it to your project::

  lektor plugin add lektor-cssbuild

Create a ``package.json`` file (the name and version aren't significant
for the plugin)::

  {
    "name": "my-project-cssbuild",
    "version": "1.0.0",
    "private": true
  }

Install uncss::

  npm install --save-dev uncss

Create a configuration file ``configs/cssbuild.ini`` and set the tool paths
(assuming that your source sass file is ``style/sass/main.scss``)::

  [sass]
  source = src:style/sass/
  output = src:assets/static/

  [uncss]
  output = dst:static/main.nested.css

  [cssmin]
  source = dst:static/main.nested.css
  output = dst:static/main.css

When writing a path, the ``src`` prefix refers to a path
in the source folders and the ``dst`` prefix refers
to the build folders.

If any tool section is missing, that tool will be skipped.

To enable the plugin during Lektor build, the ``cssbuild`` flag
has to be included (same for the ``server`` command):: 

  lektor build -f cssbuild

Using the above configuration, the build process will run as follows:

- The ``style/sass/main.scss`` file is read
  and the file ``assets/static/main.css`` is generated.

- Lektor generates the site artifacts.

- Based on the generated HTML pages, the unused CSS rules are removed
  and the result is written into the ``static/main.nested.css`` file
  *in the build directory*.

- The generated ``static/main.nested.css`` file is minified
  and the result is written into the ``main.css`` file
  in the same directory.

During uncss, the ``ignore`` option can be used to make sure
to keep some selectors::

  [uncss]
  output = src:style/css/main.css
  ignore = "/\.selector1.*/"
