import abc
import getpass
import os
from pykeepass import PyKeePass


class CredentialProvider(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_credential(self, name):
        pass


class KeepassCP(CredentialProvider):

    def __init__(self, kdbx_path, entry_titles):
        kdbx_pass = getpass.getpass("Keepass password: ")
        self.kdbx = PyKeePass(os.path.expanduser(
            kdbx_path), password=kdbx_pass)
        self.entry_titles = entry_titles

    def get_credential(self, name):
        entry_title = self.entry_titles[name]
        entry = self.kdbx.find_entries_by_title(entry_title, first=True)
        if entry is None:
            print("FATAL: No MITFCU entry found")
            sys.exit(0)
        return entry.username, entry.password


class StdinCP(CredentialProvider):

    def get_credential(self, name):
        username = input("{} username: ".format(name))
        password = getpass.getpass("{} password: ".format(name))
        return username, password
