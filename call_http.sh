#!/bin/bash

rules_resp=`curl -s 'http://192.168.31.1:9090/providers/rules' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'Authorization: Bearer 123456' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: agh_session=55c0534a8a395b76ad80718ab59667a2; _ga=GA1.1.26187587.1694322869; _ga_J69Z2JCTFB=GS1.1.1694755674.6.0.1694755725.9.0.0' \
  -H 'DNT: 1' \
  -H 'Referer: http://192.168.31.1:9090/ui/yacd/?hostname=192.168.31.1&port=9090&secret=123456' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36' \
   -compressed \
  --insecure`
providers=`echo $rules_resp | jq -r '.providers | keys | join(" ")'`

for provider in $providers
do
    echo "update $provider"
    curl 'http://192.168.31.1:9090/providers/rules/'${provider}   -X 'PUT'   -H 'Accept: */*'   -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'   -H 'Authorization: Bearer 123456'   -H 'Connection: keep-alive'   -H 'Content-Length: 0'   -H 'Content-Type: application/json'   -H 'Cookie: ph_mqkwGT0JNFqO-zX2t0mW6Tec9yooaVu7xCBlXtHnt5Y_posthog=%7B%22distinct_id%22%3A%221839bafb3c0504-072cf1f40435f5-1a525635-16a7f0-1839bafb3c11dee%22%2C%22%24device_id%22%3A%221839bafb3c0504-072cf1f40435f5-1a525635-16a7f0-1839bafb3c11dee%22%7D; agh_session=55c0534a8a395b76ad80718ab59667a2'   -H 'DNT: 1'   -H 'Origin: http://192.168.31.1:9090'   -H 'Referer: http://192.168.31.1:9090/ui/yacd/?hostname=192.168.31.1&port=9090&secret=123456'   -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'   --compressed   --insecure
done

