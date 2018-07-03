subdir('icons')

subdir('sounds')
subdir('speech')

# FIXME: Re-enable these
# # Validating the desktop file
# desktop_file_validate = find_program('desktop-file-validate', required:false)
# if desktop_file_validate.found()
#   test (
#     'Validate desktop file',
#     desktop_file_validate,
#     args: join_paths(meson.current_build_dir (), PROJECT_RDNN_NAME + '.desktop')
#   )
# endif
#
# # Validating the appdata file
# appstreamcli = find_program(['appstreamcli', 'appstream-util'], required: false)
# if appstreamcli.found()
#   test (
#     'Validate appdata file',
#     appstreamcli,
#     args: ['validate', join_paths(meson.current_build_dir (), PROJECT_RDNN_NAME + '.appdata.xml')]
#   )
# endif

# Installing the icons
# icon_sizes = ['16', '22', '32', '48', '256']
#
# foreach i : icon_sizes
#   install_data(
#     join_paths('icons/hicolor', i + 'x' + i, 'apps', PROJECT_RDNN_NAME + '.png'),
#     install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'icons', 'hicolor', i + 'x' + i, 'apps')
#   )
# endforeach
#
# custom_target('scarlettOS.desktop',
#     output : 'scarlettOS.desktop',
#     input : 'scarlettOS.desktop.in',
#     command : [intltool_merge, '--desktop-style', podir, '@INPUT@', '@OUTPUT@'],
#     install : true,
#     install_dir : get_option('datadir') + '/applications')
#
# custom_target('scarlettOS.appdata.xml',
#     output : 'scarlettOS.appdata.xml',
#     input : 'scarlettOS.appdata.xml.in',
#     command : [intltool_merge, '--xml-style', podir, '@INPUT@', '@OUTPUT@'],
#     install : true,
#     install_dir : get_option('datadir') + '/appdata')
