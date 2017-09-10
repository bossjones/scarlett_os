import errno
import os
import uuid

# source: https://github.com/Anaconda-Platform/anaconda-project/blob/b554c82fad1796e465948d032a02e69641430e07/anaconda_project/internal/rename.py
def rename_over_existing(src, dest):
    try:
        # On Windows, this will throw EEXIST, on Linux it won't.
        # on Win32 / Python 2.7 it throws OSError instead of IOError
        os.rename(src, dest)
    except (OSError, IOError) as e:
        if e.errno == errno.EEXIST:
            # Clearly this song-and-dance is not in fact atomic,
            # but if something goes wrong putting the new file in
            # place at least the backup file might still be
            # around.
            backup = dest + ".orig-" + str(uuid.uuid4())
            os.rename(dest, backup)
            try:
                os.rename(src, dest)
            except Exception as e:
                os.rename(backup, dest)
                raise e
            finally:
                try:
                    os.remove(backup)
                except Exception as e:
                    pass
        else:
            raise e
