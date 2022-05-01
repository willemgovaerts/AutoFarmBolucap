# Mac
```shell
30 * * * * /Users/willemgovaerts/Documents/bolucap/AutoFarm/venv/bin/python3 /Users/willemgovaerts/documents/bolucap/autofarm/write_data.py >> /Users/willemgovaerts/documents/bolucap/autofarm/logs/write_data.log 2>&1
```

# DO droplet
```shell
30 * * * * /home/willem/autofarm/venv/bin/python /home/willem/autofarm/write_data.py >> /home/willem/autofarm/logs/write_data.log 2>&1
```