# El País Opinion Scraper

A Python-based web scraper test that extracts articles from [El País](https://elpais.com/opinion), 
translates titles to English, and runs cross-browser automation tests using **BrowserStack**, 
orchestrated via **GitHub Actions**.

---

##  Key Features

- **Scrape** Top 5 latest opinion pieces: title, summary and cover image
- **Translate** Spanish Titles to English using Google Translate API
- **Cross-browser test** support via BrowserStack 
- **Secure credential handling** with GitHub Secrets
- **Automated CI/CD pipeline** using GitHub Actions

---

##  Table of Contents

1. [Tech Stack](#tech-stack)
2. [Project Structure](#project-structure)
3. [Live Build & Status](#live-build--status)
4. [Local Setup](#local-setup)
7. [GitHub Actions + BrowserStack](#github-actions--browserstack)
9. [Contributing](#contributing)

---

##  Tech Stack

| Technology                                                         | Purpose                                         |
| ------------------------------------------------------------------ | ----------------------------------------------- |
| [Python](https://www.python.org/)                                  | Core scripting language                         |
| [Selenium](https://www.selenium.dev/)                              | Browser automation and scraping                 |
| [Google Cloud Translation API](https://cloud.google.com/translate) | Translation API                                 |
| [BrowserStack Automate](https://www.browserstack.com/automate)     | Cross-browser cloud testing                     |
| [GitHub Actions](https://docs.github.com/en/actions)               | CI/CD and workflow automation                   |


---

##  Project Structure

```plaintext
elpais-opinion-scraper/
├── .github/
│   └── workflows/
│       └── main.yml               # GitHub Actions workflow file
├── images/
│   ├── article_1.png              # Scraped cover images
│   └── article_2.png
├── main.py                        # Main Selenium scraper
├── browserstack.yml               # BrowserStack browser/device config
├── credentials.json               # Google service account file (local only, ignored)
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
└── .gitignore                     # Ignore credentials, compiled files, outputs
```

##  Live Build & Status

[![CI Status](https://github.com/mohinia09/elpais-opinion-scraper/actions/workflows/main.yml/badge.svg)](https://github.com/mohinia09/elpais-opinion-scraper/actions)

 **Public BrowserStack Build Link**  
[View Latest Build](https://automate.browserstack.com/projects/elpais-opinion-scraper/builds/main+Commit+Merge+branch+main+of+github+elpais-opinion-scraper+Workflow:/1?public_token=8d826656f49a68f25af2ad3225803aea549754a46dc2f38a5c1a8a33cdf47873)

---

##  Local Setup

###  Requirements

- Python 3.10+
- Google Cloud project with Translation API enabled
- BrowserStack account (free or paid)

### Installation

```bash
git clone https://github.com/mohinia09/elpais-opinion-scraper.git
cd elpais-opinion-scraper
pip install -r requirements.txt
```
### Setup cedentials 
```plaintext
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
BROWSERSTACK_USERNAME=your_browserstack_username
BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key
```
### Usage
Run locally:

```bash
browserstack-sdk python main.py
```

## GitHub Actions + BrowserStack
This project runs automated CI tests on push or manual trigger.

### Required GitHub Secrets:
| Secret Name                          | Purpose                             |
| ------------------------------------ | ----------------------------------- |
| `GOOGLE_APPLICATION_CREDENTIALS_B64` | Base64-encoded service account JSON |
| `BROWSERSTACK_USERNAME`              | Your BrowserStack username          |
| `BROWSERSTACK_ACCESS_KEY`            | Your BrowserStack access key        |


### Encode the service account file:

```powershell

[Convert]::ToBase64String([IO.File]::ReadAllBytes("credentials.json")) | Set-Clipboard

```
### GitHub Workflow Example (.github/workflows/main.yml)



    - name: Restore credentials
      run: |
        echo "${{ secrets.GOOGLE_APPLICATION_CREDENTIALS_B64 }}" | base64 -d > credentials.json
        echo "GOOGLE_APPLICATION_CREDENTIALS=$PWD/credentials.json" >> $GITHUB_ENV

    - name: 'BrowserStack Env Setup'
        uses: 'browserstack/github-actions/setup-env@master'
        with:
          username:  ${{ secrets.BROWSERSTACK_USERNAME }}
          access-key: ${{ secrets.BROWSERSTACK_ACCESS_KEY }}



## Contributing
Pull requests are welcome! Please open issues for suggestions or bugs.

## Author
Mohini Aggarwal
