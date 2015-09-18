# Convert .md file to .csv

---

This is a command-line server application written in Python that uses the GitHub markdown API to convert a table in .md to .csv. The styles also come directly from GitHub, so you'll know exactly how it will appear.

## Motivation
I wanted to convert a table in .md to .csv, but I can't find any tools for it. So I just wrote one.

## Installation

### [install Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

```
$ easy_install beautifulsoup4
  or
$ pip install beautifulsoup4
```

## Usage
To convert \<filename\>.md to \<filename\>.csv : 

```
$ mdtable2csv <filename>.md
```

You will see a \<filename\>.csv in the same folder.