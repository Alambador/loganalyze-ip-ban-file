# Log Analyzer and Ip Extraction

## Premise
Each server maintains a list of attempted and successful logins. Hackers continually attempt to gain access to systems by using common login names like "root" and others. This is valuable data that should be shared between all servers on your network, and even collected in a publicly crowdsourced list eventually.

## Description

For now, this script opens a log file and searches for possible intrusion attempts. Mainly triggered by the phrase, "Failed password for". The ip address of the attempted attack is then extracted and written to a file called auto-ban.data This allows you to collect ip addresses of potential hackers without manually searching your log files.

## Roadmap

Eventually, utilizing the [fail2ban](http://fail2ban.org) this script will analyze the auth.log file for attempts to log in as root and parse out the ip address of the attacker.

This script will then extract the ip address and append the fail2ban ban file, and ban them forever.

It is meant to also be utilized along with [SaltStack](http://saltstack.org) to keep all of your servers up to date and notify each other of the attempted attacks and to ban the offending ip address.

## Requirements

- [Python](http://python.org) 2.7
- The [pyYaml](http://pyyaml.org) library for python.

## Configuration

1. Included is a default.loganalyze.cfg file
2. Copy this file and rename it to loganalyze.cfg
3. Open it in a text editor and modify the path and file locations 
for your system.
4. The loganalyze.cfg is written in yaml, so be mindful of the indentation.

## Usage

After updating your system specific configuration, you can run the file manually by issuing `python loganalyze.py` from the command-prompt, or set it to run as a [cron](http://en.wikipedia.org/cron) job at whatever interval you like. It might be a good idea to set this time to occur before your log rotations take place in order to collect enough relevant data.

## To Do

1. Use a list of phrases instead of just the individual phrase of "Failed password for". Hackers attempt to log in as "root", but also try other names of users that might not exist on your server. Log files often indicate this with, "Invalid user" followd by the user name.

2. Integrate this collection and analysis with SALT so that each minion can collect data and share it with a master. The master can then maintain the permanent ban-file and distribute it to all minions. Sharing this information between all systems can create a proactive security approach.


