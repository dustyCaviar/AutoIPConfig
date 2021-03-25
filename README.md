# AutoIPConfig
Automaticall configure machines over a serial connection using a list of IPs provided in a user created CSV file.

### How to use:
1. Make/edit the IPS_TXT file using the instructions below.
2. Connect machine via usb
3. Run the python script
4. A browser window should pop up with the GUI
5. Choose which machine you want to configure with the next machine/previous machine/text field
6. Click connect machine to initialize serial connection and parse/read over serial
7. Click configure to configure the connected machine with the ip info listed above
8. Plug the usb into the next machine and hit connect
9. Rinse and repeat

### How to format the IPs .csv file:
The script looks in it's parent directory for a file named "ips.csv".
There is an example of this .csv file in this repo.
The format for the csv file is as follows:

| MACHINE_NUMBER                    | IP                    | NETMASK                    | GATEWAY                    | RACK_NUMBER                    |
| --------------------------------- | --------------------- | -------------------------- | -------------------------- | ------------------------------ |
| {first machine's machine number}  | {first machine's IP}  | {first machine's netmask}  | {first machine's gateway}  | {first machine's rack number}  |
| {second machine's machine number} | {second machine's IP} | {second machine's netmask} | {second machine's gateway} | {second machine's rack number} |


