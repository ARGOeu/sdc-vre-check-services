# sdc-vre-check-services
Probe to check the SDC VRE Services health 

## Usage

### NAME

```
      sdc-vre-check-services.py - SDC VRE Services health  Nagios plugin
```

### SYNOPSIS

```
      sdc-vre-check-services.py  [--help] [--verbose <level>]
                   [--timeout <threshold> ] --hostname <host> [--svre <svre>] [--port <port>]
```

      Options:
       --help,-h         : Display this help.
       --verbose,-v      : Same as debug option (0-9) (supports 1 at the moment)
       --timeout,-t      : Time threshold to wait before timeout (in second).

       --hostname,-H     : The path of the vre host <name or IP).
       --svre         :  vre service to check

### OPTIONS

    --help
         Display this help.

    --verbose 
         Same as debug option.

    --timeout
         Time threshold in second to wait before timeout (default to 30).

    --hostname <host>
         The vre host . It can be a DNS name or an IP address.

    --svre <svre>
         vre service to check.


### EXAMPLES
      Using  script:

```
   ./sdc-vre-check-services.py -H www.rhost1.gr -s dashboard
```

