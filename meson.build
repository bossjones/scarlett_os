project('scarlett-os', ['c'], version: '0.1.0')

# see: https://github.com/GNOME/gnome-music/blob/88ca0fb55d5c3a035929c5d8a39c2808c27b58bd/meson.build

# pitivi way of doing it
# SOURCE: https://github.com/GNOME/pitivi/blob/b8b22123966cff0ba513300ef2b4fd3dec624c5a/meson.build
# python = find_program('python3')
# python = find_program('python3')
# intltool_merge = find_program('intltool-merge')
# itstool = find_program('itstool')
# msgfmt = find_program('msgfmt')

# Import(): Importing modules
# Imports the given extension module. Returns an opaque object that can be used to call the methods of the module. Here's an example for a hypothetical testmod module.
gnome = import('gnome')
python = import('python3')

# Make sure Python is installed and found
if not python.find_python().found()
    error('No valid python3 binary found')
endif

# FIXME: Replace this with gstreamer-espeak
# gst_transcoder_dep = dependency('gst-transcoder-1.0', version : '>= 1.8.1', fallback : ['gst-transcoder', 'gst_transcoder_dep'])
espeak_dep = dependency('espeak', fallback : ['espeak', 'espeak_dep'])

pkgdatadir = join_paths(get_option('datadir'), meson.project_name())

git = find_program('git', required : false)
if git.found()
    GITVERSION = run_command(git, 'describe', '--always').stdout().strip()
else
    GITVERSION = ''
endif

# Constants

PROJECT_NAME = meson.project_name()
API_VERSION = '0.1.0'
PROJECT_VERSION = meson.project_version()
VERSIONED_PROJECT_NAME = PROJECT_NAME+'-'+API_VERSION
CAMEL_CASE_NAME = 'ScarlettOS'
VERSIONED_CAMEL_CASE_NAME = CAMEL_CASE_NAME +'-'+ API_VERSION

PACKAGE_URL = 'https://github.com/bossjones/scarlett_os'
PACKAGE_URL_BUG = 'https://github.com/bossjones/scarlett_os'
PROJECT_RDNN_NAME='org.scarlett.ScarlettOS'

PYTHON_DIR = join_paths(get_option('prefix'), python.sysconfig_path('purelib'))
PKGDATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), PROJECT_RDNN_NAME)
PKGLIB_DIR = join_paths(get_option('prefix'), get_option('libdir'), PROJECT_RDNN_NAME)

# Dependencies

python_dep = dependency('python3', version : '>= 3.5')
gst_dep = dependency('gstreamer-1.0', version : '>= 1.8.2')
cairo_dep = dependency('cairo')
pycairo_dep = dependency('py3cairo')

dependency('gobject-introspection-1.0', version: '>= 1.35.0')
dependency('gtk+-3.0', version: '>= 3.19.3')
dependency('pygobject-3.0', version: '>= 3.21.1')
dependency('py3cairo', version: '>= 1.14.0')
dependency('grilo-0.3', version: '>= 0.3.4')

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

subdir('data')

# FIXME: This is from Pitivi, add this in to our stuff
# SOURCE: https://github.com/GNOME/pitivi/blob/b8b22123966cff0ba513300ef2b4fd3dec624c5a/meson.build
geteenvvar = find_program('getenvvar.py')
cdata = configuration_data()
cdata.set('CONFIGURED_PYTHONPATH', run_command(geteenvvar, 'PYTHONPATH').stdout().strip())
cdata.set('CONFIGURED_LD_LIBRARY_PATH', run_command(geteenvvar, 'LD_LIBRARY_PATH').stdout().strip())
cdata.set('CONFIGURED_GST_PLUGIN_PATH', run_command(geteenvvar, 'GST_PLUGIN_PATH').stdout().strip())
cdata.set('CONFIGURED_GST_PLUGIN_SYSTEM_PATH', run_command(geteenvvar, 'GST_PLUGIN_SYSTEM_PATH').stdout().strip())
cdata.set('LIBDIR', join_paths(get_option('prefix'), get_option('libdir')))
cdata.set('DATADIR', join_paths(get_option('prefix'), get_option('datadir')))
cdata.set('PACKAGE_NAME', 'ScarlettOS')
cdata.set('PACKAGE', 'scarlett')
cdata.set('GITVERSION', GITVERSION)
cdata.set('VERSION', meson.project_version())
cdata.set('BUILDDIR', meson.current_build_dir())

scarlett_os_install_dir = get_option('libdir') + '/scarlett_os/python/'

# run_command(python, '-m', 'compileall', meson.current_source_dir() + '/pitivi')
install_subdir('scarlett_os', install_dir: scarlett_os_install_dir)

# SOURCE: pitivi
configure_file(input: 'scarlett_os/configure.py.in',
               output: 'configure.py',
               configuration: cdata)

configure_file = '@0@/configure.py'.format(meson.current_build_dir())
install_data(configure_file, install_dir: scarlett_os_install_dir + 'scarlett_os')

# FIXME work around to get testsuite working
run_command('cp', configure_file, meson.current_source_dir() + '/scarlett_os')

subdir('bin')
# if not get_option('disable-help')
#     subdir('help')
# endif
subdir('tests')
