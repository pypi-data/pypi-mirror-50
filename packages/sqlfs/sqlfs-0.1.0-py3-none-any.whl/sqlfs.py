#!/usr/bin/env python3

"""SQLite FUSE filesystem.

Stores files and directories in the tables inside the SQLite database:
 - by default, maximum file size is 16 MB and number of inodes is 2^16,
 - can create in-memory filesystem without using RAM disk,
 - "df -h" should be used to estimate the amount of free space.
"""

import os
import sys
import errno
import datetime
import argparse
import logging
from pathlib import Path

import socket
import getpass
import tzlocal
import platform

import sqlite3
from sqlite3 import Error
from fuse import FUSE, FuseOSError, Operations
from stat import S_IFDIR, S_IFREG
from typing import Iterable as iterable
from types import GeneratorType as generator

'''========= HELPER FUNCTIONS ========='''


def systime() -> float:
    return datetime.datetime.utcnow().timestamp()


def version() -> str:
    return '.'.join([str(x) for x in (sqlite3.sqlite_version.split('.')[:2])])


def basedir(path: str, include_slash: bool = False) -> str:
    basedir = path[:path.rindex('/') + (1 if include_slash else 0)]
    return basedir if basedir != '' else '/'


def relname(path: str) -> str:
    return path[(path.rindex('/') + (1 if path != '/' else 0)):]


def dict_index(dictionary: dict, keys: object) -> list:
    index = []
    count = 0
    if type(keys) != list: keys = [keys]
    for k in dictionary:
        if k in keys: index.append(count)
        count += 1
    return index


def list_index(collection: list, keys: object) -> list:
    if type(keys) != list: keys = [keys]
    return[collection.index(k) for k in keys]


'''========= CACHE ANNOTATIONS ========='''


def cache_add(argument, parent=False):
    def decorator(function):
        global cache
        global cache_size
        def push(*args):
            if cache is None: return function(*args)
            if len(cache) > cache_size: cache.clear()
            key = [args[1:][i] for i in list_index(function.__code__.co_varnames[1:function.__code__.co_argcount], argument)]
            if len(key) != 1:
                raise OSError('Cache key must be scalar')
            else:
                key = key[0]
            if parent: key = basedir(key)
            entry = cache.get(key, {})
            func = function.__name__
            if entry.get(func, None) is None:
                entry[func] = function(*args)
                if type(entry[func]) == generator: entry[func] = [x for x in entry[func]]
            if not (key in cache): cache[key] = entry
            return entry[func]
        return push
    return decorator


def cache_drop(argument, include_parent=False, root=False):
    def decorator(function):
        global cache
        def pop(*args):
            if cache is None: return function(*args)
            keys = [args[1:][i] for i in list_index(function.__code__.co_varnames[1:function.__code__.co_argcount], argument)]
            if include_parent: keys.extend([basedir(k) for k in keys])
            if root: keys.append('/')
            for key in keys: cache.pop(key, None)
            return function(*args)
        return pop
    return decorator


'''========= MAIN CLASS ========='''


class SQLFS(Operations):

    max_name_length = 255
    strict_dir_pointers = True
    LOG_FORMAT = '%(asctime)-15s %(name)s %(levelname)-8s %(message)s'

    def __init__(self,
                 path: 'path to SQLite database',
                 block_size: '512 bytes' = 0x200,
                 max_filesize: '16 MB' = 0x1000000,
                 max_inodes: '65536' = 0x10000,
                 with_cache: 'enable cache' = True,
                 cache_size: '8192' = 8192,) -> None:
        self.id = 0x501F5
        self.path = path
        self.block_size = block_size
        self.max_filesize = max_filesize
        self.max_inodes = max_inodes
        self.with_cache = with_cache
        self.cache_size = cache_size
        self.creation_date = datetime.datetime.now(tzlocal.get_localzone()).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.creation_user = getpass.getuser()
        self.creation_host = socket.gethostname()
        self.sqlite_version = version()
        self.python_version = sys.version
        self.os_type = platform.system()+' ('+sys.platform+')'
        self.os_kernel = platform.release()
        self.os_arch = platform.machine()
        self.os_release = platform.version()
        attributes = {}
        for attribute in self.__dict__:
            attributes[attribute] = getattr(self, attribute)
        if os.path.isdir(self.path): raise FuseOSError(errno.EMEDIUMTYPE)
        exists = os.path.exists(self.path)
        corrupted = True
        try:
            self.connection = sqlite3.connect(self.path)
            self.log.info('SQLite database connected')
        except Error as e:
            raise e
        statement = self.connection.cursor()
        if not exists:
            self.log.warning('Creating tables, as SQLite database does not exist')
            statement.execute("create table sqlfs(attribute_name text not null, attribute_value text)")
            statement.execute("create table directories(id integer primary key, parent integer,"
                              "atime real, ctime real, mtime real, nlink integer not null, path text not null)")
            statement.execute("create table files(id integer primary key, dir integer not null, "
                              "atime real, ctime real, mtime real, size integer not null, name text not null, data blob, FOREIGN KEY (dir) REFERENCES directories(id))")
            self.log.debug('Created tables, inserting data')
            statement.execute('insert into directories(path,atime,ctime,mtime,nlink) values (?,?,?,?,?)', ('/', systime(), systime(), systime(), 2))
            for k, v in attributes.items():
                statement.execute('insert into sqlfs values (?,?)', (k, repr(v),))
            corrupted = False
            self.log.warning('Created tables with initial structure')
        if corrupted:
            self.log.info('Checking data consistency')
            statement.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
            rows = statement.fetchall()
            if len(rows) == 3:
                corrupted = False
            attributes = ['id', 'block_size', 'max_filesize', 'max_inodes', 'with_cache', 'cache_size', 'creation_date', 'creation_user', 'creation_host', ]
            statement.execute('select * from sqlfs')
            for name, value in statement.fetchall():
                if not name in attributes: continue
                if name == 'with_cache':
                    setattr(self, name, value == str(True))
                elif name.startswith('creation'):
                    setattr(self, name, str(value))
                else:
                    setattr(self, name, int(value))
        statement.close()
        self.connection.commit()
        if corrupted:
            self.log.critical("SQLFS is corrupted")
            raise OSError(errno.ENOMEDIUM, "Filesystem is corrupted")
        self.statement = None
        self.log.info('Created SQLFS')
        pass

    @classmethod
    def init_log(cls: object, logfile: str, level: object) -> None:
        if level != logging.CRITICAL: logging.basicConfig(format=cls.LOG_FORMAT, filename=logfile, filemode='a+')
        cls.log = logging.getLogger(Path(__file__).name)
        cls.log.setLevel(level)

    '''========= HELPER METHODS ========='''

    def _handle(self):
        if self.statement is not None:
            return self.statement
        self.statement = self.connection.cursor()
        self.log.debug('Created SQL statement')
        return self.statement

    def _sync(self):
        if self.statement is not None:
            self.statement.close()
            self.connection.commit()
        self.statement = None
        self.log.debug('Flushed data')
        return 0

    def _get_record(self, *args):
        self.log.debug('Executing SQL: %s', repr(args))
        self._handle().execute(*args)
        for cell, in self._handle().fetchall():
            return cell
        return None

    def _get_row(self, *args):
        self.log.debug('Executing SQL: %s', repr(args))
        self._handle().execute(*args)
        for row in self._handle().fetchall():
            return row
        return None

    def _process_cells(self, *args, function=lambda x: x):
        self.log.debug('Executing SQL: %s', repr(args))
        self._handle().execute(*args)
        for cell, in self._handle().fetchall():
            function(cell)

    # Filesystem Operations
    # =====================

    '''========= FILESYSTEM METHODS ========='''

    def init(self, path: 'always /') -> 'initialize filesystem':
        self.log.info('Initializing')
        global cache
        global cache_size
        if self.with_cache:
            cache = {}
        else:
            cache = None
        cache_size = self.cache_size
        self.log.info('SQLFS properties:')
        for attribute in self.__dict__:
            value = getattr(self, attribute)
            if type(value) in tuple([str, int, bool]):
                self.log.info('    %s: %s', attribute, str(value).replace('\n',' '))
        self.log.warning('Mounted filesystem')
        inodes = []
        self._process_cells('select count(1) from directories union select count(1) from files', function=lambda c: inodes.append(c))
        count = sum(inodes) - 1
        self.log.warning("Number of occupied inodes: %d", count)

    def destroy(self, path: 'always /') -> 'destroy filesystem':
        self._sync()
        self.connection.close()
        self.log.warning('Unmounted filesystem')

    @cache_add('path')
    def statfs(self, path: 'always /') -> dict:
        self.log.info('"%s" is called for path [%s]', 'statvfs', path)
        inodes = []
        self._process_cells('select count(1) from directories union select count(1) from files', function=lambda c: inodes.append(c))
        count = sum(inodes) - 1
        free = int((self.max_filesize * (self.max_inodes - count)) / self.block_size)
        return {'f_bsize': self.block_size, 'f_frsize': self.block_size, 'f_fsid': self.id, 'f_flag': 4096, 'f_blocks': int((self.max_filesize * self.max_inodes) / self.block_size),
                'f_bavail': free, 'f_bfree': free, 'f_files': self.max_inodes, 'f_ffree': self.max_inodes - count, 'f_favail': self.max_inodes - count, 'f_namemax': self.max_name_length}

    '''========= DIR AND FILE METHODS ========='''

    @cache_add('path')
    def getattr(self, path: str, fh: int = None) -> dict:
        self.log.info('"%s" is called for path [%s], fd [%s]', 'getattr', path, str(fh))
        attributes = ['st_atime', 'st_ctime', 'st_mtime', 'st_nlink', 'st_gid', 'st_uid', 'st_blocks', 'st_blksize', 'st_size', 'st_mode']
        dir = self._get_row('select * from directories where path = ?', (path,))
        if dir is not None:
            _, _, atime, ctime, mtime, nlinks, _ = dir
            return dict(zip(attributes, (atime, ctime, mtime, nlinks, 0, 0, 0, self.block_size, 0, S_IFDIR | 0o0777)))  # st_mode drwxrwxrwx = 0o40777
        parent = self._get_record('select id from directories where path = ?', (basedir(path),))
        if parent is not None:
            file = self._get_row('select atime,ctime,mtime,size from files where name = ? and dir = ? order by id asc', (relname(path), parent,))
            if file is not None:
                atime, ctime, mtime, size = file
                return dict(zip(attributes, (atime, ctime, mtime, 1, 0, 0, int(size / self.block_size) + 1, self.block_size, size, S_IFREG | 0o0777)))  # st_mode -rwxrwxrwx = 0o100777
        raise FuseOSError(errno.ENOENT)

    def getxattr(self, path, name, position=0):
        self.log.debug('"%s" is called for path [%s], name [%s], position [%s]', 'getxattr', path, str(name), str(position))
        raise FuseOSError(errno.ENOTSUP)

    def setxattr(self, path, name, value, options, position=0):
        self.log.debug('"%s" is called for path [%s], name [%s], value [%s], options [%s], position [%s]', 'setxattr', path, str(name), str(value), str(options), str(position))
        raise FuseOSError(errno.ENOTSUP)

    def listxattr(self, path):
        self.log.debug('"%s" is called for path [%s]', 'listxattr', path)
        return []

    def removexattr(self, path, name):
        self.log.debug('"%s" is called for path [%s], name [%s]', 'removexattr', path, str(name))
        raise FuseOSError(errno.ENOTSUP)

    @cache_drop(['old', 'new'], include_parent=True)
    def rename(self, old: str, new: str) -> int:
        self.log.info('"%s" is called for old path [%s], new path [%s]', 'move', old, new)
        if old == '/' or new == '/': raise FuseOSError(errno.EIO)
        if self._get_record('select id from directories where path = ?', (new,)) is not None: raise FuseOSError(errno.EEXIST)
        new_parent = self._get_record('select id from directories where path = ?', (basedir(new),))
        if new_parent is None: raise FuseOSError(errno.ENOENT)
        fid = self._get_record('select f.id from files f inner join directories d on f.dir=d.id where f.name = ? and d.path = ?', (relname(new), basedir(new),))
        if fid is not None: self.unlink(new)
        old_parent = 0
        dir = self._get_row('select id, parent from directories where path = ?', (old,))  # in case directory is moved
        if dir is not None:
            id, old_parent = dir
            self._handle().execute('update directories set atime = ?, mtime = ?, path = ?, parent = ? where id = ?', (systime(), systime(), new, new_parent, id,))
            self._process_cells('select path from directories where path like ?', ((old + '/%'),),
                                function=lambda path: self._handle().execute('update directories set path = ? where path = ?', (path.replace(old, new, 1), path,)))
        file = self._get_row('select f.id, f.dir from files f inner join directories d on f.dir=d.id where f.name = ? and d.path = ?', (relname(old), basedir(old),))  # in case file is moved
        if file is not None:
            id, old_parent = file
            self._handle().execute('update files set atime = ?, name = ?, dir = ? where id = ?', (systime(), relname(new), new_parent, id,))
        self._handle().execute('update directories set atime = ?, mtime = ?, nlink = nlink + 1 where id = ?', (systime(), systime(), new_parent))
        self._handle().execute('update directories set atime = ?, mtime = ?, nlink = nlink - 1 where id = ?', (systime(), systime(), old_parent))
        self._sync()
        return 0

    def access(self, path: str, mode: int) -> int:  # modes: 4-read, 2-write
        self.log.info('"%s" is called for path [%s], mode [%d]', 'access', path, mode)
        return 0

    def chmod(self, path: str, mode: int) -> int:  # modes: 4-read, 2-write, 1-exec
        self.log.info('"%s" is called for path [%s], mode [%d]', 'chmod', path, mode)
        return 0

    def chown(self, path: str, uid: int, gid: int) -> int:  # default: uid=1000,gid=1000, root: uid=0,gid=0
        self.log.info('"%s" is called for path [%s], uid [%d], gid [%d]', 'chown', path, uid, gid)
        return 0

    def ioctl(self, path, cmd, arg, fip, flags, data):
        self.log.debug('"%s" is called for path [%s], cmd [%s], arg [%s], fip [%s], flags [%s], data [%s]',
                       'ioctl', path, str(cmd), str(arg), str(fip), str(flags), str(data))
        raise FuseOSError(errno.ENOTTY)

    def mknod(self, path, mode, dev):  # FIFO pipes, etc are not supported
        self.log.debug('"%s" is called for path [%s], mode [%d], dev [%s]', 'mknod', path, mode, str(dev))
        raise FuseOSError(errno.ENOTSUP)

    '''========= DIRECTORY METHODS ========='''

    @cache_add('path')
    def opendir(self, path: str) -> int:
        self.log.info('"%s" is called for path [%s]', 'opendir', path)
        id = self._get_record('select id from directories where path = ?', (path,))
        if id is None: raise FuseOSError(errno.ENOENT)
        return id

    @cache_add('path')
    def readdir(self, path: str, fh: int) -> iterable[str]:
        self.log.info('"%s" is called for path [%s], fd [%d]', 'readdir', path, fh)
        dirents = ['.', '..']
        if self.strict_dir_pointers:
            id = self._get_record('select id from directories where path = ? and id = ?', (path, fh,))
        else:
            id = self._get_record('select id from directories where path = ?', (path,))
        if id is None: raise FuseOSError(errno.ENOENT)
        self._process_cells('select name from files where dir = ?', (id,), function=lambda name: dirents.append(name))
        self._process_cells('select path from directories where parent = ?', (id,), function=lambda dir: dirents.append(relname(dir)))
        for r in dirents:
            yield r

    def releasedir(self, path: str, fh: int) -> int:
        self.log.info('"%s" is called for path [%s], fd [%d]', 'releasedir', path, fh)
        return self._sync()

    @cache_drop('path', include_parent=True, root=True)
    def mkdir(self, path: str, mode: int) -> int:
        self.log.warning('"%s" is called for path [%s], mode [%d]', 'mkdir', path, mode)
        if path == '/': raise FuseOSError(errno.EEXIST)  # short circuit
        if self._get_record('select id from directories where path = ?', (path,)) is not None: raise FuseOSError(errno.EEXIST)
        id = self._get_record('select id from directories where path = ? or path like ?', (basedir(path), basedir(path, include_slash=True)))
        if id is None: raise FuseOSError(errno.ENOENT)
        inodes = []
        self._process_cells('select count(1) from directories union select count(1) from files', function=lambda c: inodes.append(c))
        if sum(inodes) > self.max_inodes: raise FuseOSError(errno.ENOSPC)
        if len(relname(path)) > self.max_name_length: raise FuseOSError(errno.ENAMETOOLONG)
        self._handle().execute('insert into directories(parent,path,atime,ctime,mtime,nlink) values (?,?,?,?,?,?)', (id, path, systime(), systime(), systime(), 2))
        self._handle().execute('update directories set nlink = nlink + 1, atime = ?, mtime = ? where id = ?', (systime(), systime(), id,))
        self._sync()
        return 0

    @cache_drop('path', include_parent=True, root=True)
    def rmdir(self, path: str) -> int:
        self.log.warning('"%s" is called for path [%s]', 'rmdir', path)
        if path == '/': raise FuseOSError(errno.ENOTEMPTY)  # short circuit
        dir = self._get_row('select id,nlink,parent from directories where path = ?', (path,))
        if dir is None: raise FuseOSError(errno.ENOENT)
        id, nlink, parent = dir
        if (nlink > 2): raise FuseOSError(errno.ENOTEMPTY)
        self._handle().execute('delete from directories where id = ?', (id,))
        self._handle().execute('update directories set nlink = nlink - 1 , atime = ?, mtime = ? where id = ?', (systime(), systime(), parent,))
        self._sync()
        return 0

    def fsyncdir(self, path, datasync, fh) -> int:
        self.log.info('"%s" is called for path [%s], datasync [%s], fh [%s]', 'fsyncdir', path, str(datasync), str(fh))
        return self._sync()

    '''========= FILE METHODS ========='''

    @cache_drop('path', include_parent=True, root=True)
    def create(self, path: str, mode: int, fi: int = None) -> int:
        self.log.warning('"%s" is called for path [%s], mode [%d], fi [%s]', 'create', path, mode, str(fi))
        inodes = []
        self._process_cells('select count(1) from directories union select count(1) from files', function=lambda c: inodes.append(c))
        if sum(inodes) > self.max_inodes: raise FuseOSError(errno.ENOSPC)
        id = self._get_record('select f.id from files f inner join directories d on f.dir=d.id where f.name = ? and d.path = ?', (relname(path), basedir(path),))
        if id is not None: return id
        parent = self._get_record('select id from directories where path = ?', (basedir(path),))
        if parent is None: raise FuseOSError(errno.ENOENT)
        if len(relname(path)) > self.max_name_length: raise FuseOSError(errno.ENAMETOOLONG)
        self._handle().execute('insert into files(dir,atime,ctime,mtime,size,name) values (?,?,?,?,?,?)', (parent, systime(), systime(), systime(), 0, relname(path)))
        self._handle().execute('update directories set atime = ?, mtime = ?, nlink = nlink + 1 where id = ?', (systime(), systime(), parent,))
        self._sync()
        id = self._get_record('select f.id from files f inner join directories d on f.dir=d.id where f.name = ? and d.path = ?', (relname(path), basedir(path),))
        if id is not None: return id
        return -1

    @cache_drop('path', include_parent=True, root=True)
    def unlink(self, path: str) -> int:
        self.log.warning('"%s" is called for path [%s]', 'unlink', path)
        file = self._get_row('select f.id,f.dir from files f inner join directories d on f.dir=d.id where f.name = ? and d.path = ?', (relname(path), basedir(path),))
        if file is None: raise FuseOSError(errno.ENOENT)
        id, parent = file
        self._handle().execute('delete from files where id = ?', (id,))
        self._handle().execute('update directories set atime = ?, mtime = ?, nlink = nlink - 1 where id = ?', (systime(), systime(), parent,))
        self._sync()
        return 0

    @cache_add('path')
    def open(self, path: str, flags: int) -> int:
        self.log.info('"%s" is called for path [%s], flags [%d]', 'open', path, flags)
        if (flags & 0x0400): self.truncate(path, 0)
        id = self._get_record('select f.id from files f inner join directories d on f.dir=d.id where f.name = ? and d.path = ?', (relname(path), basedir(path),))
        if id is not None:
            self._handle().execute('update files set atime = ? where id = ?', (systime(), id))
            self._sync()
            return id
        raise FuseOSError(errno.ENOENT)

    def release(self, path: str, fh: int) -> int:
        self.log.info('"%s" is called for path [%s], fd [%d]', 'close', path, fh)
        return self._sync()

    def read(self, path: str, length: int, offset: int, fh: int) -> bytes:
        self.log.info('"%s" is called for path [%s], length [%d], offset [%d], fh [%d]', 'read', path, length, offset, fh)
        file = None
        if fh is not None and fh > 0:
            file = self._get_row('select id,name,size,data from files where id = ?', (fh,))
        else:
            file = self._get_row('select f.id,f.name,f.size,f.data from files f inner join directories d on f.dir=d.id where f.name = ? and d.path = ?', (relname(path), basedir(path),))
        if file is not None:
            id, name, size, data = file
            if relname(path) != name: raise FuseOSError(errno.EBADF)
            self._handle().execute('update files set atime = ? where id = ?', (systime(), id,))
            if data is None: return bytes()
            return data[offset:min(size, offset + length)]
        else:
            raise FuseOSError(errno.ENOENT)

    @cache_drop('path')
    def write(self, path: str, data: bytes, offset: int, fh: int) -> int:
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug('"%s" is called for path [%s], offset [%d], fh [%d], data [%s]', 'write', path, offset, fh, repr(data))
        else:
            self.log.info('"%s" is called for path [%s], offset [%d], fh [%d]', 'write', path, offset, fh)
        if fh is not None and fh > 0:
            file = self._get_row('select id,name,size,data from files where id = ?', (fh,))
        else:
            file = self._get_row('select f.id,f.name,f.size,f.data from files f inner join directories d on f.dir=d.id where f.name = ? and d.path = ?', (relname(path), basedir(path),))
        if file is not None:
            id, name, size, filedata = file
            if relname(path) != name: raise FuseOSError(errno.EBADF)
            if filedata is None: filedata = bytes()
            buffer = bytearray()
            buffer[:offset] = filedata[:offset]
            buffer[offset:(offset + len(data))] = data
            if len(filedata) > offset + len(data): buffer[offset + len(data):] = filedata[offset + len(data):]
            if len(buffer) > self.max_filesize: raise FuseOSError(errno.ENOMEM)
            self._handle().execute('update files set atime = ?, mtime = ?, size = ?, data = ? where id = ?', (systime(), systime(), len(buffer), buffer, id,))
            self._sync()
            return len(data)
        else:
            raise FuseOSError(errno.ENOENT)

    def flush(self, path: str, fh: int) -> int:
        self.log.info('"%s" is called for path [%s], fd [%d]', 'flush', path, fh)
        return self._sync()

    def fsync(self, path: str, fdatasync: object, fh: int) -> int:
        self.log.info('"%s" is called for path [%s], datasync [%s], fh [%s]', 'fsync', path, str(fdatasync), str(fh))
        return self._sync()

    @cache_drop('path')
    def truncate(self, path: str, length: int, fh: int = None) -> int:
        self.log.info('"%s" is called for path [%s], length [%d], fh [%s]', 'truncate', path, length, str(fh))
        if fh is not None and fh > 0:
            file = self._get_row('select id,name,size,data from files where id = ?', (fh,))
        else:
            file = self._get_row('select f.id,f.name,f.size,f.data from files f inner join directories d on f.dir=d.id where f.name = ? and d.path = ?', (relname(path), basedir(path),))
        if file is not None:
            id, name, size, filedata = file
            if relname(path) != name: raise FuseOSError(errno.EBADF)
            if filedata is not None:
                filedata = filedata[:length]
            else:
                filedata = bytes()
            self._handle().execute('update files set atime = ?, mtime = ?, size = ?, data = ? where id = ?', (systime(), systime(), length, filedata, id,))
            self._sync()
        else:
            raise FuseOSError(errno.ENOENT)
        return 0

    @cache_drop('path')
    def utimens(self, path: str, times: tuple = None) -> int:
        self.log.info('"%s" is called for path [%s], times [%s]', 'utimens', path, str(times))
        if times is None: times = (systime(), systime())
        id = self._get_record('select f.id from files f inner join directories d on f.dir=d.id where f.name = ? and d.path = ?', (relname(path), basedir(path),))
        if id is not None: self._handle().execute('update files set atime = ?, mtime = ? where id = ?', (times[0], times[1], id,))
        return 0

    '''========= LINK METHODS ========='''

    def symlink(self, name: str, target: str) -> int:  # symbolic links are not supported
        self.log.info('"%s" is called for name [%s], target [%s]', 'symlink', name, target)
        raise FuseOSError(errno.ENOTSUP)

    def link(self, target: str, name: str) -> int:  # hard links are not supported
        self.log.info('"%s" is called for name [%s], target [%s]', 'link', name, target)
        raise FuseOSError(errno.ENOTSUP)

    def readlink(self, path: str) -> str:
        self.log.info('"%s" is called for path [%s]', 'readlink', path)
        return path


'''========= END MAIN CLASS ========='''


class ArgFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__, formatter_class=ArgFormatter,
                                     epilog="Run \"fusermount -u mount\" to unmount.")
    g = parser.add_argument_group("SQLFS settings")
    g.add_argument("--block-size", metavar="B", default=0x200, type=int, help="Filesystem block size, in bytes")
    g.add_argument("--max-filesize", metavar="F", default=0x1000000, type=int, help="Maximum file size, in bytes")
    g.add_argument("--max-inodes", metavar="I", default=0x10000, type=int, help="Maximum number of inodes")
    g.add_argument("--use-cache", metavar="C", default='Y', type=str, help="Use in-memory cache, 'Y' (yes) or 'N' (no)")
    g.add_argument("--cache-size", metavar="N", default=8192, type=int, help="If above is set to Y, cache size")
    g.add_argument("--log-file", metavar="L", default='sqlfs.log', type=str, help="Log file")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--debug", "-d", action="store_true", default=False, help="Enable debug logging")
    g.add_argument("--verbose", "-v", action="store_true", default=False, help="Enable verbose logging")
    g.add_argument("--quiet", "-q", action="store_true", default=True, help="Normal logging")
    g.add_argument("--silent", "-s", action="store_true", default=False, help="No logging")
    parser.add_argument("path", type=str, help="Path to the SQLite v3 database with the filesystem, or 'memory' for the in-memory filesystem")
    parser.add_argument("mount", type=str, help="Mount point directory")
    return parser.parse_args(args)


def main():
    options = parse_args()
    level = logging.WARNING
    level = logging.DEBUG if options.debug else level
    level = logging.INFO if options.verbose else level
    level = logging.CRITICAL if options.silent else level
    SQLFS.init_log(options.log_file, level)
    FUSE(SQLFS(':memory:' if options.path == 'memory' else options.path, max_inodes=options.max_inodes,
               with_cache='Y' == options.use_cache, cache_size=options.cache_size,
               block_size=options.block_size, max_filesize=options.max_filesize),
         options.mount, nothreads=True, foreground=True)
    pass


if __name__ == '__main__':
    main()

#
