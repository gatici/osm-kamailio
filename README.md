# Kamailio SIP Server Deployment by OSM
#### https://www.kamailio.org/w/
#### Kamailio® (successor of former OpenSER and SER) is an Open Source SIP Server released under GPLv2+, able to handle thousands of call setups per second. 
#### Kamailio can be used to build large platforms for VoIP and realtime communications – presence, WebRTC, Instant messaging and other applications.

## Clone the repository

```bash
git clone https://github.com/gatici/osm-kamailio.git && pushd osm-kamailio
```

## Clone the charms

```bash
./charms/kamailio-bundle/clone_charms.sh
```

## Build the charms under charms folder.

```bash 
./charms/kamailio-bundle/build.sh
``` 

## Deploy the Charms with Juju (Optional)
This process could be done after charms are cloned and built according to main guide.

## Prepare environment for Juju Deployment (Optional)

```bash
juju add-model kamailio
```

## Deploy with Juju (Optional)

Deploy bundle:

```bash
./charms/kamailio-bundle/deploy_bundle.sh
```

## Copy built charms into kamailio_cnf.

Copy charms in to CNF folder in order to instantiate a Network Service through OSM:

```bash
./charms/kamailio-bundle/copy.sh
```

## Onboarding through OSM

## Upload Packages
```bash
./upload.sh
```

## Create Service
vim_account_name=your_prefered_vim_account
```bash
./onboard.sh $vim_accunt_name
```

## Remove Packages
```bash
./remove_packages.sh
```
