configure_file(input: 'scarlett.in',
               output: 'scarlett',
               configuration: cdata)

scarlett_bin = '@0@/scarlett'.format(meson.current_build_dir())
install_data(scarlett_bin, install_dir: get_option('bindir'))

# Create `scarlett` in the current dir at build time to be able to
# run uninstalled in the dev env.
run_command('cp', scarlett_bin, meson.current_source_dir())
