#!/usr/bin/env python3
# coding=utf-8
import json
import os

import requests
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient


def get_domain_list():
    """
    获取需要解析的域名
    :return:
    """
    abs_path = os.path.dirname(os.path.abspath(__file__))
    with open(abs_path + '/config.json', 'r+') as file:
        config = json.load(file)

    return config


def get_outer_net_ip():
    """
    获取外网IP
    :return:
    """
    return requests.get('http://ip.360.cn/IPShare/info').json()['ip']


def get_domain_record(client, domain, rr):
    """
    获取解析记录
    :param client
    :param domain:
    :param rr:
    :return:
    """
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain)
    request.set_KeyWord(rr)

    response = client.do_action_with_exception(request)
    records = json.loads(response)['DomainRecords']['Record']

    if len(records) > 0:
        for item in records:
            if item['RR'] == rr:
                return item

    return None


def add_domain_record(client, domain, rr, value):
    """
    新增解析记录
    :param client
    :param domain:
    :param rr:
    :param value:
    :return:
    """
    request = AddDomainRecordRequest()
    request.set_DomainName(domain)
    request.set_RR(rr)
    request.set_Type('A')
    request.set_Value(value)

    response = client.do_action_with_exception(request)
    return response


def update_domain_record(client, record_id, rr, value):
    """
    更新解析记录
    :param client
    :param record_id:
    :param rr:
    :param value:
    :return:
    """
    request = UpdateDomainRecordRequest()
    request.set_RecordId(record_id)
    request.set_RR(rr)
    request.set_Type('A')
    request.set_Value(value)

    response = client.do_action_with_exception(request)
    return response


def ddns():
    """
    更新记录
    :return:
    """
    ip = get_outer_net_ip()
    if ip is None:
        return {
            'status': 'failed',
            'message': '获取公网IP失败'
        }

    domain_list = get_domain_list()
    modified = []
    for item in domain_list:
        ak, secret, domain, prefix = item['ak'], item['secret'], item['domain'], item['prefix']
        client = AcsClient(ak, secret)
        try:
            record = get_domain_record(client, domain, prefix)
            if (record is None) or (record['Value'] != ip):
                # 更新IP
                update_domain_record(client, record['RecordId'], prefix, ip) if record else \
                     add_domain_record(client, domain, prefix, ip)
                # 记录修改记录
                modified.append({
                    'status': 'successful',
                    'full_domain': prefix + '.' + domain,
                    'original': record['Value'] if record else '',
                    'current': ip
                })
        except Exception as e:
            modified.append({
                'status': 'failed',
                'message': str(e),
                'full_domain': prefix + '.' + domain
            })

    return modified


if __name__ == '__main__':

    print(json.dumps(ddns()))
