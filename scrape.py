import urllib2
import re
import csv
import argparse

def Get_HTML_From_URL(url):
    decoded = url.decode("utf-8")
    ascii_url = decoded.encode("ascii", "ignore")
    response = urllib2.urlopen(ascii_url)
    html = response.read()
    return html

def Get_ID_From_Name(lastname, firstname):

    number = ""
    url = 'http://www.cincybar.org/news-resources/legal-directory.php?firstname={1}&lastname={0}'.format(lastname, firstname)
    html = Get_HTML_From_URL(url)

    match = re.search(r'legal-directory.php/([0-9]*)', html, flags=0)
    if match != None:
        number = match.group(1)
    else:
        number = ""

    return number


def Get_Phone_From_Id(pid):

    phone = ""

    url = 'http://www.cincybar.org/news-resources/legal-directory.php/{0}'.format(pid)
    html = Get_HTML_From_URL(url)
    match = re.search(r'itemprop="tel">([^<]*)</strong>', html, flags=0)

    if match != None:
        phone = match.group(1)
    else:
        phone = ""

    return phone


def main():
    parser = argparse.ArgumentParser(description='Scrape the Cincinnati Bar website for phone numbers from a CSV list of names')
    parser.add_argument('source', nargs=1, help='Source filename -- CSV containing a list of names.  Formatted Firstname, Lastname.')
    parser.add_argument('outfile', nargs=1, help='Output filename -- CSV Containing a list of names with phone numbers')
    args = parser.parse_args()

    source = args.source[0]
    outfile = args.outfile[0]


    outrows = []
    with open(source, 'rb') as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in r:
            firstname = row[0]
            lastname = row[1]
            truncate_position = lastname.find(",")
            person_id = ""
            phone = ""
            if truncate_position == -1:
                lastname_truncated = lastname
            else:
                lastname_truncated = lastname[:truncate_position]

            person_id = Get_ID_From_Name(lastname_truncated.lower(), firstname.lower())

            if person_id != "":
                phone = Get_Phone_From_Id(person_id)

            outrows.append([firstname, lastname, phone])
    
    with open(outfile, 'w') as csv_outfile:
        writer = csv.writer(csv_outfile)
        writer.writerows(outrows)



            #print "{0},{1},{2}".format(lastname, firstname, thisphone)

if __name__ == "__main__":
    main()