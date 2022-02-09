from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
import time
from requests import ConnectionError, HTTPError
from urllib import error
from shared_lists import device_list
# for writing to a different directory
import os.path

dt = datetime.now().time()
dt = dt.replace(microsecond=0)
dt_date = datetime.now().date()

file_format_time = str(dt).replace(':', '_')
file_format_date = str(dt_date).replace('-', '_')

current_date = (dt_date.strftime('%m/%d/%Y'))  # formatting date to mm/dd/yyy

# orth = ['71', '72', '73', '74', '75', '76', '77', '78', '79', '80',
#        '87', '88', '92', '100', '96', '95', '97', '135', '105', '106']

theurl = 'https://w1.weather.gov/obhistory/PAQT.html'
thepage = urllib.request.urlopen(theurl)
soup = BeautifulSoup(thepage, features="lxml")
current_temp = soup.find_all('td')[14].text
current_temp = int(current_temp)
canadian_temp = (current_temp - 32) * (5 / 9)
local_weather = (str(current_temp) + 'F/' + str(int(canadian_temp)) + 'C')

absolute_path = 'C:/Users/pboynto/PycharmProjects/orthogon_reporting/output_logs/'
filename = f'log_{file_format_date}_{file_format_time}.txt'
complete_name_and_path = os.path.join(absolute_path, filename)

def main():
    with open(complete_name_and_path, 'w') as f:
        print('{:^70}{:^70}{:^70}'.format(('.' * 10), ('.' * 10), ('.' * 10)))
        f.write('{:^70}{:^70}{:^70}'.format(('.' * 10), ('.' * 10), ('.' * 10)) + '\n')
        print('{:^70}{:^70}{:^70}'.format(local_weather, current_date, str(dt)))
        f.write('{:^70}{:^70}{:^70}'.format(local_weather, current_date, str(dt)) + '\n')
        print('{:^70}{:^70}{:^70}'.format(('.' * 10), ('.' * 10), ('.' * 10)))
        f.write('{:^70}{:^70}{:^70}'.format(('.' * 10), ('.' * 10), ('.' * 10)) + '\n')
        print('*' * 210)
        f.write('*' * 210 + '\n')
        print('{:<20}{:^15}{:^25}{:^15}{:^15}{:^45}{:^50}{:>20}'.format('Linkname', 'IP', 'Site', 'TX Power/Max', 'RSSI',
                                                                        'TX MOD/RX MOD', 'Modulation Detail',
                                                                        'Link Capacity'))
        f.write('{:<20}{:^15}{:^25}{:^15}{:^15}{:^45}{:^50}{:>20}'.format('Linkname', 'IP', 'Site', 'TX Power/Max', 'RSSI',
                                                                          'TX MOD/RX MOD', 'Modulation Detail',
                                                                          'Link Capacity') + '\n')
        print('*' * 210 + '\n')
        f.write(('*' * 210 + '\n'))
        for o in device_list.devices:
            try:
                s = (f'10.27.11.{o}')
                url_address = 'http://' + str(s) + '/top.cgi?xsrf=&1'
                status_page = urllib.request.urlopen(url_address)
                status = BeautifulSoup(status_page, features='lxml')
                hostname = status.find('div', id='pageBody').find('div', id='linkName').get('title')

                site_name = status.find('div', id='pageBody').find('div', id='siteName').text.strip('\n')
                tx_power = status.find('div', id='pageBody').find_all('tr')[7].find_all('td')[3].text
                max_tx_power = status.find('div', id='pageBody').find_all('tr')[5].find_all('td')[5].text.strip('\n')
                hardware = status.find('div', id='pageBody').find('div', id='hardwareVersion').get('title')
                if hardware.startswith('B'):
                    try:
                        rx_power = status.find('div', id='pageBody').find_all('div')[26].text.strip(',')
                        tx_mod = status.find('div', id='pageBody').find_all('tr')[22].find_all('td')[5].text
                        rx_mod = status.find('div', id='pageBody').find_all('tr')[23].find_all('td')[5].text
                        link_capacity = status.find('div', id='pageBody').find_all('tr')[21].find_all('td')[5].text.strip(
                            '\n')
                        mod_detail = status.find('div', id='pageBody').find_all('tr')[25].find_all('td')[5].text.strip('\n')
                    except:
                        mod_detail = status.find('div', id='pageBody').find_all('tr')[25].find_all('td')[3].text.strip('\n')
                elif hardware.startswith('D'):
                    rx_power = status.find('div', id='pageBody').find_all('div')[25].text.strip(',')
                    tx_mod = status.find('div', id='pageBody').find_all('tr')[19].find_all('td')[5].text
                    rx_mod = status.find('div', id='pageBody').find_all('tr')[20].find_all('td')[5].text
                    link_capacity = status.find('div', id='pageBody').find_all('tr')[18].find_all('td')[5].text.strip('\n')
                    mod_detail = status.find('div', id='pageBody').find_all('tr')[22].find_all('td')[5].text.strip('\n')
                    time.sleep(.25)
                tx_mod = tx_mod.split()  # removing duplicates
                tx_mod = tx_mod[0:2]
                tx_mod = ' '.join(tx_mod)
                print('{:<20}{:^15}{:^25}{:^15}{:^15}{:^45}{:^50}{:>20}'.format(hostname, s, site_name,
                                                                                (tx_power + '/' + max_tx_power),
                                                                                rx_power, (tx_mod + '/' + rx_mod),
                                                                                mod_detail, (link_capacity + 'Mbps')))
                f.write('{:<20}{:^15}{:^25}{:^15}{:^15}{:^45}{:^50}{:>20}'.format(hostname, s, site_name,
                                                                                  (tx_power + '/' + max_tx_power),
                                                                                  rx_power, (tx_mod + '/' + rx_mod),
                                                                                  mod_detail,
                                                                                  (link_capacity + 'Mbps')) + '\n')
                print('-' * 210)
                f.write('-' * 210 + '\n')
                time.sleep(1)
                f.write('\n')
            except(ConnectionError, TimeoutError, Exception) as e:
                print(s + ' has experienced a ' + str(e))
                f.write(str(e) + '\n')
                continue
            except HTTPError as e:
                print(e)
                f.write(e)
                f.write('\n')
                continue
            except urllib.error.URLError:
                print(s + 'is offline')
                f.write(s + 'is offline' + '\n')
                continue

if __name__ == '__main__':
    main()
