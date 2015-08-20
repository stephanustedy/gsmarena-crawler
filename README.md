# GSM Arena Phones Crawler
Phone Crawlers using Kimonolabs web service APIs.
This app uses Python 3 scripting.

## Usage

### Crawling Data
To crawl data from Kimonolabs, type the following script:
```
python3 crawlPhone.py -p
```

To populate phone urls from local file `phones/phone_list.txt" and crawl the links directly, type:
```
python3 crawlPhone.py
```

By default, the crawler automatically pass data that has been crawled. If you want to recrawl from the beginning, type:
```
python3 crawlPhone.py -nc
```
*Remember that this will need a lot of time to finish.*

### Format Data
To format the crawled data to CSV, type the following:
```
python3 formatPhone.py <formatted_input_filename> [csv_output_filename.csv]
```
If you don't specify `csv_output_filename.csv`, the script will prompt the CSV filename after formatting.

Most of the time, you will run:
```
python3 formatPhone.py processors/formatted-data.json IntelProcessor.csv
```

## Additional Notes
This project is originally created for Tokopedia usage and is now open-sourced.
Feel free to reformat the raw data to your styling by editing `src/IntelProcessor.py`