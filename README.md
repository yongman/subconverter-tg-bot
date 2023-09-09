# A simple bot for quick add/delete proxy rules for clash

In my scenario, it's works with subconverter for subscription. The bot can deploy in the same host with subconverter and mount the subconverter's rules directory.
Set the following envrionment variables first,
- `TOKEN`: the telegram bot token
- `FILE_NAME`: rulesets file path to update
- `POST_CMD`: a shell command to call `clash` http API, named `call_http.sh`

call_http.sh example
```shell
curl 'http://{ip}:9090/providers/rules/Proxy_domain'   -X 'PUT'   -H 'Accept: */*'   -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'   -H 'Authorization: Bearer {secret}'   -H 'Connection: keep-alive'   -H 'Content-Length: 0'   -H 'Content-Type: application/json'   -H 'Cookie: ph_mqkwGT0JNFqO-zX2t0mW6Tec9yooaVu7xCBlXtHnt5Y_posthog=%7B%22distinct_id%22%3A%221839bafb3c0504-072cf1f40435f5-1a525635-16a7f0-1839bafb3c11dee%22%2C%22%24device_id%22%3A%221839bafb3c0504-072cf1f40435f5-1a525635-16a7f0-1839bafb3c11dee%22%7D; agh_session=55c0534a8a395b76ad80718ab59667a2'   -H 'DNT: 1'   -H 'Origin: http://{ip}:9090'   -H 'Referer: http://ip:9090/ui/yacd/?hostname={ip}&port=9090&secret={secret}'   -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'   --compressed   --insecure
```

1. `/add example.com` add domain suffix to rulesets file and call `POST_CMD`
2. `/del example.com` delete domain suffix from rulesets file and call `POST_CMD`
