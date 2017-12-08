import os

def get_xdg_data_home():
    if 'XDG_DATA_HOME' in os.environ:
        d = os.environ['XDG_DATA_HOME']
    else:
        if 'HOME' in os.environ:
            home = os.environ['HOME']
        else:
            home = os.path.expanduser('~')
        d = home + '/.local/share'

    return d

def get_xdr_data_dirs():
    if 'XDG_DATA_DIRS' in os.environ:
        dirs = os.environ['XDG_DATA_DIRS']
    else:
        dirs = '/usr/local/share/:/usr/share/'
    return dirs.split(':')


if __name__ == '__main__':
    print("xdg_data_home: %s" % get_xdg_data_home())
    print("xdr_data_dirs: %s" % get_xdr_data_dirs())
