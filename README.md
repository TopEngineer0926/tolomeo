# Tolomeo

Project with the scope of map the darkweb via snowball scraping technique, with a UI simple and comfortable. Donated to the Istituto Nazionale di Criminologia di Vibo Valentia, Italy.

## Getting Started

### Got the Makefile
In order to start the project locally you need to know what is in the Makefile:
- run `make help` in project root folder, you will be noticed with the main functionalities.

### Run containers and frontend locally
To set all your containers up:
- run `make up`.

## Scan the found onion site
Simply run `make scan onion_site=fakesite.onion` specifying the *onion_site* to be scan and you will get an export of vulnerabilities of the site in *scan_result.log* file.

We use Onionscan for the purpose, please see https://onionscan.org/ for more info.

## In production
Build everything running `make up-production`and go to *localhost:80*...enjoy!
