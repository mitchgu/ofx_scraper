import glob
import os
from time import sleep

def scrape_mitfcu(scd, credentials, accounts):
    BASE_URL = "https://www.mitfcu.org"
    DOWNLOAD_PATH = "Transactions.ofx"
    SELECTORS = {
        "login_frame": "iframe[title='Online Banking Login']",
        "username": "input#userid",
        "password": "input#password",
        "login": "button[type=submit]",
        "dash_frame": "uspbody",
        "account": "a[data-name={}]",
        "table": "table.cardlytics_transaction_table",
        "datepicker": "table#lblMenuDateRanges",
        "start_date": "input#startdt",
        "end_date": "input#enddt",
        "date_submit": "div#pnlCustomDate button:last-child",
        "export": "table#downloadLink button",
        "ofx_radio": "input[type=radio]#OFX",
        "download": ".exportMenuFooter button",
    }
    username, password = credentials

    scd.get(BASE_URL)
    scd.switch_to_frame(scd.find(SELECTORS["login_frame"]))
    scd.fill_field(SELECTORS["username"], username)
    scd.fill_field(SELECTORS["password"], password)
    scd.find(SELECTORS["login"]).click()

    def scrape_account(name):
        scd.wait_till_clickable(SELECTORS["account"].format(acct_name)).click()
        scd.wait_till_visible(SELECTORS["table"])
        scd.find(SELECTORS["datepicker"]).click()
        scd.fill_field(SELECTORS["start_date"], "01/01/2014")
        scd.find(SELECTORS["date_submit"]).click()
        scd.wait_till_visible(SELECTORS["table"])
        scd.wait_till_clickable(SELECTORS["export"]).click()
        scd.wait_till_clickable(SELECTORS["ofx_radio"]).click()
        scd.wait_till_clickable(SELECTORS["download"]).click()

    for acct_name, dest_file in accounts.items():
        [os.remove(f) for f in glob.glob("Transactions*.ofx")]
        scd.switch_to_frame(SELECTORS["dash_frame"])
        scrape_account(acct_name)
        while not os.path.exists(DOWNLOAD_PATH):
            sleep(0.1)
        os.rename(DOWNLOAD_PATH, dest_file + ".ofx")
        scd.refresh()
