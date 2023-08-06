#!/usr/bin/python3


###
# Collection of functions useful for Managed Mac scripts
# JWRN3 - July 2019
###

__author__ = 'jwrn3@cam.ac.uk'

# Import modules required
import os
import subprocess
import sys
import socket
import CoreFoundation
import platform
import shlex
from SystemConfiguration import SCDynamicStoreCopyConsoleUser

# Variables & Constants
jamf_binary = '/usr/local/jamf/bin/jamf'
systemsetup_binary = '/usr/sbin/systemsetup'
scutil_binary = '/usr/sbin/scutil'


# Get IP address
def get_ip_address():
    """Get the IP address of the host."""

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('1.1.1.1', 1))
        ip_address = s.getsockname()[0]
    except socket.error:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address


# Get FQDN
def get_fqdn():
    """Return the FQDN."""

    ip_address = get_ip_address()
    if ip_address:
        try:
            fqdn = socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            return None
        else:
            return fqdn


# Get hostname
def get_hostname():
    """Return the Mac hostname."""

    ip_address = get_fqdn()
    hostname = get_fqdn().split('.')[0] if ip_address else None
    return hostname


# Get MCS site
def get_site():
    """Return the MCS site"""

    ip_address = get_fqdn()
    site = get_fqdn().split('.')[1] if ip_address else None
    return site


# Get console user
def get_console_user():
    """Get current console user"""

    username, uid, gid = (
        SCDynamicStoreCopyConsoleUser(None, None, None) or [None])
    return [username, ""][username in [u"loginwindow", None, u""]]


# Get console user UID
def get_console_user_uid():

    """Get current console user"""
    username, uid, gid = (
        SCDynamicStoreCopyConsoleUser(None, None, None) or [None])
    return uid


# Get console user GID
def get_console_user_gid():
    """Get current console user"""

    username, uid, gid = (
        SCDynamicStoreCopyConsoleUser(None, None, None) or [None])
    return gid


# Run command
def run_command(command):
    """Run command supplied"""

    # Pass a string such as 'ls -al /path/to/myfile'
    # to shlex.split() and it will be tokenised.

    tokenised_command = shlex.split(command)

    try:
        subprocess.run(tokenised_command,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       close_fds=True,
                       check=True)

    except subprocess.CalledProcessError as error:
        log_err('Error code: {}'.format(error.returncode))
        return False

    except OSError as error:
        log_err('Error: {} ({})'.format(error.strerror, error.errno))
        return False

    return True


# Run command and return output
def get_command_output(command):
    """Run the command and return the output"""

    tokenised_command = shlex.split(command)

    try:
        result = subprocess.run(tokenised_command,
                                capture_output=True,
                                check=True)

    except subprocess.CalledProcessError as error:
        log_err('Error: {}, ({})'.format(error.output, error.returncode))
        return None

    except OSError as error:
        log_err('Error: {} ({})'.format(error.strerror, error.errno))
        return None
    else:
        return result.stdout.decode('utf-8')


# Get preferences key from defaults
def get_prefs_key(prefs_key, CFPrefsBundle):
    """Get the preferences key from CFPrefs"""

    return CoreFoundation.CFPreferencesCopyAppValue(
            prefs_key, CFPrefsBundle)


# Set preferences key in defaults
def set_prefs_key(prefs_key, prefs_value, CFPrefsBundle):

    """Set the preferences key in CFPrefs"""
    CoreFoundation.CFPreferencesSetAppValue(
            prefs_key, prefs_value, CFPrefsBundle)


# Set complex preferences key in defaults
def set_complex_prefs_key(prefs_key, prefs_value, CFPrefsBundle, userdomain,
                          hostdomain):

    """Set the preferences key in CFPrefs

        userdomain can be one of
        kCFPreferencesCurrentUser or kCFPreferencesAnyUser

        hostdomain can be one of
        kCFPreferencesCurrentHost or kCFPreferencesAnyHost"""
    CoreFoundation.CFPreferencesSetValue(
            prefs_key, prefs_value, CFPrefsBundle, userdomain, hostdomain)


# Sync CFPrefs
def sync_prefs(CFPrefsBundle):
    """Sync CFPrefs to disk"""

    CoreFoundation.CFPreferencesAppSynchronize(
            CFPrefsBundle)


# Log INFO message
def log_info(message):

    """Log a message to STDOUT"""
    print(message)


# Log to STDERR
def log_err(*args, **kwargs):

    """Log a message to STDERR"""
    print(*args, file=sys.stderr, **kwargs)


# Return major macOS version
def get_major_macos_version():
    """Return major macOS version"""

    return platform.mac_ver()[0].split('.')[1]


# Return minor macOS version
def get_minor_macos_version():
    """Return minor macOS version"""

    return platform.mac_ver()[0].split('.')[2]


# Are we running as through Self Service?
def self_service():
    """Return true if the script is running through Jamf Pro Self Service"""

    if not os.environ.get('USERNAME') and os.environ.get('USER'):
        return True
    else:
        return False
