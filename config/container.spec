{
       "Image": "dockable/app",
       "Labels": {
               "com.example.vendor": "giohan",
               "com.example.license": "GPL",
               "com.example.version": "0.0.1"
       },
       "Volumes": {
         "/volumes/data": {}
       },
       "NetworkDisabled": false,
       "ExposedPorts": {
               "22/tcp": {},
               "8080/tcp": {}
       },
       "StopSignal": "SIGTERM",
       "HostConfig": {
         "Binds": ["/tmp:/tmp","/container-logs:/var/log/application"],
         "CpuPercent": 80,
         "CpuShares": 512,
         "CpuPeriod": 100000,
         "CpuQuota": 50000,
         "CpusetCpus": "0",
         "CpusetMems": "0",
         "MaximumIOps": 0,
         "MaximumIOBps": 0,
         "BlkioWeight": 300,
         "MemorySwappiness": 60,
         "PublishAllPorts": true,
         "ReadonlyRootfs": false,
         "NetworkMode": "bridge",
         "LogConfig": { "Type": "json-file", "Config": {} }
      }
}
