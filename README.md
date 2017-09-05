# zabbix-templates-generic
Some generic Zabbix templates. Mainly used for process monitoring.

In addition, some templates are improvements from the default template
## Template OS Linux
Naming changes (grouping)
Swap space monitored by used space. Not pct free (looks better in graphs)
Number of CPU added to alert high load on systems more accuratly
Check if iptables is running
Changed the way memory is monitored.
  Get total memory and available memory. Then calculate used mem as total - available
Several triggers modified to display more information
Modified some graphs:
- memory usage renamed to memory utilization
  - shows memory used and total in stead of memory free
- Swap usage
  - Show swap used and total in stead of swap free
- Added Processes
  - Shows max number of processes, number of processes and number of running processes

Discovery:
 - Mounted filesystem discovery
   - Removed free disk space percentage
   - Added additional trigger for disk space usage. Also enhanced description of trigger. It now displays the disk values and host name.
   - Modifed graph from pie displaying free space to normal graphs, displaying used space

## Template JMX Kafka
Used to monitor Kafka message brokers using JMX.

### Installation
- Place the files "/Template JMX Kafka/jmx_discovery" and "/Templates JMX Kafka/JMXDiscovery-0.0.1.jar" in the externalscripts folder of the Zabbix-server (default location: /usr/lib/zabbix/externalscripts)
- Import the template Template JMX Kafka.xml into Zabbix server
- Add JMX interface to host
- Assign template to host

## Template Zookeeper
Used to monitor Zookeeper nodes using mntr.

### Installation
- Place the file "Template Zookeeper/getZookeeperInfo.py" in the externalscripts folder of the Zabbix-server (default location: /usr/lib/zabbix/externalscripts)
- Import the template Template Zookeeper.xml into Zabbix server
- Assign template to host