# trafficlight  
  
start and stop ec2 instances.  
  
### installation  
  
##### install with pip  
  
`pip install trafficlight`  
  
### dependencies   
  
-aws cli (installed and configured)  
-python3     

### flags  
```
  -h, --help     show this help message and exit  
  --key KEY      optional. use a tag key besides Name  
  -g, --green    start all.  
  -r, --red      stop all.  
  -y, --yes      automatically approve instance state change.  
  -H, --host     use hostnames instead of ip addresses.  
  -v, --version  show program's version number and exit  
```
  
### usage  
  
show trafficlight help page, including usage and flags.  
`$ trafficlight -h`  
   
switch instance with tag Name:example. if instance is stopped it will start, if it's running it will stop.   
`$ trafficlight example`   
   
start all instances with tag Name:example. if instances are started already they will stay up.   
`$ trafficlight example -g`   
   
stop all instances tag Name:example. if instances are stopped already they will stay stopped.   
`$ trafficlight example -r`   
   
stop all instances with tag Products:example.    
`$ trafficlight example --key Products -r`   
   
list all ec2s and do nothing.  
`$ trafficlight`  
  
list all ec2s and stop them.  
`$ trafficlight -r`  
