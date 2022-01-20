# Kamailio SIP Server Deployment by OSM
#### https://www.kamailio.org/w/
#### Kamailio® (successor of former OpenSER and SER) is an Open Source SIP Server released under GPLv2+, able to handle thousands of call setups per second. 
#### Kamailio can be used to build large platforms for VoIP and realtime communications – presence, WebRTC, Instant messaging and other applications.

## Charm Preparation

### Build the charms under charms folder.

```bash 
./charms/kamailio-bundle/build.sh
``` 

### Copy built charms into kamailio_cnf.

```bash
./charms/kamailio-bundle/copy.sh
```

## Onboarding through OSM

### Upload Packages
```bash
./upload.sh
```

### Create Service
```bash
./onboard.sh
```

### Remove Packages
```bash
./remove_packages.sh
```
