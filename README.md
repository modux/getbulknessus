# getbulknessus


Handy script to retrieve results from Nessus scans in bulk. 

```
>getnessusbulk.py --help
usage: getnessusbulk.py [-h] [--sleep SLEEP] --url URL -l LOGIN -p PASSWORD -f
                        {csv,nessus,html} [--debug DEBUG] [-o OUTPUT]
                        FOLDER

Download Nesuss results in bulk

positional arguments:
  FOLDER                Folder from which to download

optional arguments:
  -h, --help            show this help message and exit
  --sleep SLEEP         poll/sleep timeout
  --url URL, -u URL     url to nessus instance, default https://localhost:8834
  -l LOGIN, --login LOGIN
                        Nessus login
  -p PASSWORD, --password PASSWORD
                        Nessus password
  -f {csv,nessus,html}, --format {csv,nessus,html}
                        Format of nesuss output, defaults to csv
  --debug DEBUG         Enable debugging output
  -o OUTPUT, --output OUTPUT
                        Output directory
```
