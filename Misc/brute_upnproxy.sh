#!/bin/bash
url=$1
soap_head='<?xml version="1.0" encoding="utf-8"?><s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><u:GetGenericPortMappingEntry xmlns:u="urn:upnporg:serviceId:WANIPConnection.1#GetGenericPortMappingEntry"><NewPortMappingIndex>'
soap_tail='</NewPortMappingIndex></u:GetGenericPortMappingEntry></s:Body></s:Envelope>'
for i in `seq 0 10`; do
payload=$soap_head$i$soap_tail
curl -H 'Content-Type: "text/xml;charset=UTF-8"' -H 'SOAPACTION: "urn:schemasupnp-org:service:WANIPConnection:1#GetGenericPortMappingEntry"' --data "$payload" "$url"
echo ""
done

# ./brute_upnproxy.sh http://192.168.1.1:2048/etc/linuxigd/gatedesc.xml