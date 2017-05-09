from credential_providers import KeepassCP, StdinCP
import os
from scrapers import scrape_mitfcu
from selenium import webdriver
from simple_driver import SimpleChromeDriver
import sys
import yaml


def get_config():
    with open('config.yaml', 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as e:
            print(e)
            abort()


def get_cp(c):
    if c["credential_provider"] == "keepass":
        try:
            return KeepassCP(c["keepass"]["kdbx_path"],
                             c["keepass"]["entry_titles"])
        except IOError as e:
            print("Error opening Keepass database:", e)
            abort()
    elif c["credential_provider"] == "stdin":
        return StdinCP()
    else:
        print("Invalid credential provider type")
        abort()


def get_scd(profile_path=None):
    if(profile_path):
        co = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : os.getcwd()}
        co.add_experimental_option("prefs", prefs)
        co.add_argument("user-data-dir=" + profile_path)
        return SimpleChromeDriver(chrome_options=co)
    else:
        return SimpleChromeDriver()


def abort():
    print("Exiting...")
    sys.exit(0)

if __name__ == "__main__":
    c = get_config()
    cp = get_cp(c)
    scd = get_scd(c["chrome_profile_path"])
    try:
        for t in c["targets"]:
            credentials = cp.get_credential(t["name"])
            if t["name"] == "MITFCU":
                scrape_mitfcu(scd, credentials, t["accounts"])
            else:
                print("Target {} not supported".format(t["name"]))
                abort()
    except KeyboardInterrupt as e:
        pass
    scd.quit()
