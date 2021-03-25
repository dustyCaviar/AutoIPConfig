# AutoIPConfig
Automaticall configure machines over a serial connection using a list of IPs provided in a user created CSV file.

### How to format the IPs .csv file:
The script looks in it's parent directory for a file named "ips.csv".
There is an example of this .csv file in this repo.
The format for the csv file is as follows:

| MACHINE_NUMBER                    | IP                    | NETMASK                    | GATEWAY                    | RACK_NUMBER                    |
| --------------------------------- | --------------------- | -------------------------- | -------------------------- | ------------------------------ |
| {first machine's machine number}  | {first machine's IP}  | {first machine's netmask}  | {first machine's gateway}  | {first machine's rack number}  |
| {second machine's machine number} | {second machine's IP} | {second machine's netmask} | {second machine's gateway} | {second machine's rack number} |


