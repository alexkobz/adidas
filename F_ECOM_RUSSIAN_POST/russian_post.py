import csv
import sys
import pandas
import requests
import xml.etree.ElementTree as ElementTree
from datetime import datetime, timedelta
import re


def body(number, login, password):
    body = \
        """<?xml version="1.0" encoding="UTF-8"?>
        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:oper="http://russianpost.org/operationhistory" xmlns:data="http://russianpost.org/operationhistory/data" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
           <soap:Header/>
           <soap:Body>
              <oper:getOperationHistory>
                 <data:OperationHistoryRequest>
                    <data:Barcode>""" + number + """</data:Barcode>
                    <data:MessageType>0</data:MessageType>
                    <data:Language>RUS</data:Language>
                 </data:OperationHistoryRequest>
                 <data:AuthorizationHeader soapenv:mustUnderstand="1">
                    <data:login>""" + login + """</data:login>
                    <data:password>""" + password + """</data:password>
                 </data:AuthorizationHeader>
              </oper:getOperationHistory>
           </soap:Body>
        </soap:Envelope>"""

    return body


def write(et):
    ns = {'ns7': 'http://russianpost.org/operationhistory', 'ns3': 'http://russianpost.org/operationhistory/data'}
    flag, type, attr, date, postmat_type, postmat_attr, postmat_date = 0, 0, 0, 0, 0, 0, 0
    for i in et.findall('.//ns7:getOperationHistoryResponse/ns3:OperationHistoryData/ns3:historyRecord', ns):
        type = i.find('ns3:OperationParameters/ns3:OperType/ns3:Id', ns).text
        attr = i.find('ns3:OperationParameters/ns3:OperAttr/ns3:Id', ns).text
        date = i.find('ns3:OperationParameters/ns3:OperDate', ns).text

        # прибытие в пункт выдачи
        if int(type) == 8 and int(attr) == 2:
            postmat_type, postmat_attr, postmat_date = type, attr, date
            flag = 1

        # финальные статусы
        if int(type) == 2 and int(attr) in (1, 2, 4, 6, 7, 8, 9, 13, 18):
            flag = 2
            break
        elif int(type) == 3 and int(attr) in (1, 2, 10, 11):
            flag = 2
            break
        elif int(type) == 5 and int(attr) in (1, 2):
            flag = 2
            break
        elif int(type) == 26 and int(attr) == 1:
            flag = 2
            break

    if flag == 1:
        return flag, postmat_type, postmat_attr, postmat_date

    return flag, type, attr, date


def main():
    url = 'https://tracking.russianpost.ru/rtm34'
    headers = {"Content-Type": "application/soap+xml; charset=utf-8"}
    basefolder = sys.argv[1]
    login = sys.argv[2]
    password = sys.argv[3]

    df = pandas.read_csv(basefolder + "shipment_in.csv")
    data = df.iloc[:, 0].astype(str).str.split(';', expand=True)
    data.columns = df.columns[0].split(';')
    orders = pandas.Series(data.iloc[:, 0]).tolist()
    shipment = pandas.Series(data.iloc[:, 1]).tolist()
    if not orders or not shipment:
        sys.exit("\"shipment\" parameter is required")

    csv_file_path = basefolder + "shipment_out.csv"
    file = open(csv_file_path, "w", newline='')
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        "ORDER_NO",
        "SHIPMENT_NO",
        "STATUS_CODE",
        "STATUS_DATE"
    ])

    for order, number in zip(orders, shipment):
        msg = body(number, login, password)
        response = requests.post(url, data=msg, headers=headers)
        et = ElementTree.fromstring(response.content)
        flag, type, attr, date = write(et)
        if flag:
            t = date.replace('T', ' ')
            t = re.sub(r'[.](\d\d\d)[+]', '', t)
            date = datetime.strptime(t[:-5], "%Y-%m-%d %H:%M:%S") + timedelta(hours=int(t[-5:].replace(':00', '')))
            writer.writerow([
                order,
                number,
                str(str(type) + str(attr)),
                date
            ])
    file.close()


if __name__ == '__main__':
    main()
