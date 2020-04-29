# RxAnimDownloader
> extract all links of the anime that you search
## Installation
-  Clone the project in your computer
-  Download python 3
-  Install scrapy : `pip install scrapy`
-  with your terminal, move to the directory /rxanimdowloader/rxanimdowloader
-  Run the command `scrapy crawl anime -o conan.json -a search="Detective Conan"`
-  You can see the a created file with name conan.json (Here are all download link for each episode of Detective Conan)
## Make a multiple download
-   with the terminal, move to the root directory
-   Run the command ``python downloader.py conan.json`` (conan.json is the file generated previously)