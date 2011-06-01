#!/usr/bin/env python
import pynotify
import subprocess
import sys
import json
import glib

def get_path():
    return '/'.join(__file__.split('/')[:-1]) + '/'

config = json.loads(open(get_path() + 'autosshfs.json').read())

if __name__ == '__main__':
    notify = False
    if pynotify.init("SSHFS Mounter"):
        notify = True
    try:
        if sys.argv[1] == 'mount':
            for share in config['shares']:
                args = [
                    'sshfs',
                    share[0],
                    share[1]
                ]
                try:
                    subprocess.check_output(args)
                    n = pynotify.Notification("AutoSSHFS Mounted",
                        '%s on %s' % (share[0], share[1]))
                except subprocess.CalledProcessError:
                    n = pynotify.Notification("AutoSSHFS Mount Failed",
                        '%s' % (share[0]))
                try:
                    n.set_timeout(1)
                    n.show()
                except glib.GError:
                    print "Failed to open display."
        elif sys.argv[1] == 'unmount':
            for share in config['shares']:
                args = [
                    'fusermount',
                    '-u',
                    share[1]
                ]
                try:
                    subprocess.check_output(args)
                    n = pynotify.Notification("AutoSSHFS Unmounted",
                        '%s from %s' % (share[0], share[1]))
                except subprocess.CalledProcessError:
                    n = pynotify.Notification("AutoSSHFS Unmount Failed",
                        '%s' % (share[0]))
                try:
                    n.set_timeout(1)
                    n.show()
                except glib.GError:
                    print "Failed to open display."
    except IndexError:
        print "Usage: %s [mount|unmount]" % sys.argv[0]
