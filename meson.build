project('scarlett-os',
    version: '0.1.0'
)

# Import(): Importing modules
# Imports the given extension module. Returns an opaque object that can be used to call the methods of the module. Here's an example for a hypothetical testmod module.
gnome = import('gnome')
i18n  = import('i18n')
python = import('python3')

# Make sure Python is installed and found
if not python.find_python().found()
    error('No valid python3 binary found')
endif

# Constants
PACKAGE_URL = 'https://github.com/bossjones/scarlett_os'
PACKAGE_URL_BUG = 'https://github.com/bossjones/scarlett_os'
PROJECT_RDNN_NAME='org.scarlett.Listener'

PYTHON_DIR = join_paths(get_option('prefix'), python.sysconfig_path('purelib'))
PKGDATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), PROJECT_RDNN_NAME)
PKGLIB_DIR = join_paths(get_option('prefix'), get_option('libdir'), PROJECT_RDNN_NAME)

# Dependencies
dependency('gobject-introspection-1.0', version: '>= 1.35.0')
# dependency('gtk+-3.0', version: '>= 3.19.3')
# dependency('libmediaart-2.0', version: '>= 1.9.1')
# dependency('tracker-sparql-2.0', version: '>= 1.99.1')
dependency('pygobject-3.0', version: '>= 3.21.1')
dependency('py3cairo', version: '>= 1.14.0')
# dependency('grilo-0.3', version: '>= 0.3.4')

# Subproject(): Takes the project specified in the positional argument and brings that
# in the current build specification by returning a subproject object.
# Subprojects must always be placed inside the subprojects directory at
# the top source directory. So for example a subproject called foo must be
# located in ${MESON_SOURCE_ROOT}/subprojects/foo. Supports the following
# keyword arguments:
# subproject('libgd',
#     default_options: [
#         'with-introspection=true',
#         'with-main-view=true',
#         'with-tagged-entry=true',
#         'static=false',
#         'pkgdatadir=' + PKGDATA_DIR,
#         'pkglibdir=' + PKGLIB_DIR
#    ])

# subdir('data')
# subdir('help')
# subdir('po')

install_subdir(
    'scarlett_os',
    install_dir: PYTHON_DIR
)

# Install the executable file
# configuration_data(): Creates an empty configuration object. You should add your configuration
# with its method calls and finally use it in a call to configure_file.
bin_config = configuration_data()
bin_config.set('rdnn_name', PROJECT_RDNN_NAME)
bin_config.set('pkgdatadir', PKGDATA_DIR)
bin_config.set('localedir', join_paths(get_option('prefix'), get_option('datadir'), 'locale'))
bin_config.set('pythondir', PYTHON_DIR)
bin_config.set('pyexecdir', join_paths(get_option('prefix'), python.sysconfig_path('stdlib')))
bin_config.set('schemasdir', '')
# Used for libgd
bin_config.set('pkglibdir', PKGLIB_DIR)

bin_config.set('local_build', 'False')

configure_file(
    input: 'scarlett_os.in',
    output: 'scarlettOS',
    configuration: bin_config,
    install_dir: get_option('bindir')
)

# Install the builddir executable
local_config = configuration_data()
local_config.set('rdnn_name', PROJECT_RDNN_NAME)
local_config.set('pkgdatadir', join_paths(meson.build_root(), 'data'))
local_config.set('localedir', join_paths(get_option('prefix'), get_option('datadir'), 'locale'))
local_config.set('pythondir', meson.source_root())
local_config.set('pyexecdir', meson.source_root())
local_config.set('schemasdir', join_paths(meson.build_root(), 'data'))
# Used for libgd
# local_config.set('pkglibdir', join_paths(meson.build_root(), 'subprojects', 'libgd', 'libgd'))

local_config.set('local_build', 'True')

configure_file(
    input: 'scarlett_os.in',
    output: 'scarlett_os_tasker',
    configuration: local_config
)

# meson.add_postconf_script('meson_post_conf.py')
# meson.add_install_script('meson_post_install.py')
