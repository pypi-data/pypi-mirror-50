# -*- coding: utf-8 -*-

from __future__ import print_function

import grpc
from dns import resolver
from dns.exception import DNSException
from pro.protos import promotion_pb2, promotion_pb2_grpc

# 连接consul服务，作为dns服务器
consul_resolver = resolver.Resolver()
consul_resolver.port = 8600
consul_resolver.nameservers = ["172.16.9.144"]


serviceName = "promotion-service"


def get_ip_port():
    '''查询出可用的一个ip，和端口'''
    try:
        dnsanswer = consul_resolver.query(serviceName + ".service.consul", "A")
        dnsanswer_srv = consul_resolver.query(serviceName + ".service.consul", "SRV")
    except DNSException:
        return None, None
    return dnsanswer[0].address, dnsanswer_srv[0].port


_HOST, _PORT = get_ip_port()
print(_HOST, _PORT)


def run():
    channel = grpc.insecure_channel(_HOST + ':' + str(_PORT))
    client = promotion_pb2_grpc.ComputeStub(channel=channel)

    message = 'python22哈哈'
    response = client.handle(promotion_pb2.PromotionRequest(message=message))
    print("received: " + response.message)


if __name__ == '__main__':
    run()
