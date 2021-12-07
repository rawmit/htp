# htp
A simple Http/Https proxy server scanner:

This tool was written in 2020 for testing proxy-servers speed.

This tool does not needed any extra module(just python3 default modules).

Modules used:
<li>os</li>
<li>socket</li>
<li>argparse</li>        
<li>re</li>
<li>time</li>
        
# How to use:
After clone;

By run <b>python3 htp.py -h</b> you will be get how to use htp.

<h3>arguments:</h3>
<b>--password-list PATH_OF_PASSWORD_LIST</b> This part just for generate the passwords(This part is not very usable but it can be better with updates).

<b>-config PATH_OF_CONFIGS_FILE</b> Path of configs file(configs will be use in password-list generating), Default: "htp-data/config.ini".

<b>-out PATH_OF_FILE_FOR_WRITE_PASSWORD_OUT</b> Path of file for write generated passwords with your patterns in configs file, Default: "htp-data/output.pwl".

<b>-scan PATH_OF_FILE_FOR_WRITE_OUT</b> Path of file for save scanned http and https proxies to that file.

<b>-http PATH_OF_FILE_FOR_WRITE_OUT</b> Path of file for save scanned http proxies to that file.

<b>-https PATH_OF_FILE_FOR_WRITE_OUT</b> Path of file for save scanned https proxies to that file.

<b>-l</b> Show log.
