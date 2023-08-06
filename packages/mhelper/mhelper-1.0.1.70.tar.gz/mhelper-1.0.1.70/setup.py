from distutils.core import setup


def readme():
    with open( 'readme.rst' ) as f:
        return f.read()


setup( name = "mhelper",
       url = "https://bitbucket.org/mjr129/mhelper",
       version = "1.0.1.70",
       description = "Includes a collection of utility functions.",
       long_description = readme(),
       author = "Martin Rusilowicz",
       license = "https://www.gnu.org/licenses/agpl-3.0.html",
       python_requires = ">=3.7",
       include_package_data = True,

       packages = ["mhelper",
                   "mhelper.mannotation",
                   "mhelper_qt",
                   "mhelper_qt.designer",
                   "mhelper.unittests"
                   ],


       extras_require = { 'all'       : ["jsonpickle",
                                         "PyQt5",
                                         "mistune",
                                         ],
                          'deprecated': ["py-flags"]
                          }
       )
