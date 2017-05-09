# OFX scraper
A tool for automatically scraping OFX files from banking sites with Selenium.

Right now it only supports MITFCU because that's the only thing I care about

## Getting started

1. `pip install -r requirements.txt` (in a virtualenv if you want)
2. Copy `config_example.yaml` to `config.yaml` and configure it how you want (pretty self explanatory)
3. `python main.py`

## Features
* Reading credentials from a keepass database or from stdin
* MITFCU support
  * Note that on the first run, MITFCU will want to confirm your identity through phone or email since you're running an unfamiliar browser profile, which will crash the scraper. Once you follow directions and register the selenium browser as your private computer, MITFCU will remember your browser fingerprint and it'll work on subsequent runs.

## Requirements
* `chromedriver` executable in your path.