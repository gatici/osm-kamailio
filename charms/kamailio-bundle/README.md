# Kamailio Operators
#### https://www.kamailio.org/w/
#### Kamailio® (successor of former OpenSER and SER) is an Open Source SIP Server released under GPLv2+, able to handle thousands of call setups per second. 
#### Kamailio can be used to build large platforms for VoIP and realtime communications – presence, WebRTC, Instant messaging and other applications.

## Prepare environment

```bash
juju add-model kamailio
```

## Deploy with Juju

Build charms:

```bash
./build.sh
```

Deploy bundle:

```bash
juju deploy ./bundle.yaml --trust
```

## Preparation for deployment with OSM

Copy charms in to CNF folder in order to instantiate a Network Service through OSM:

```bash
./copy.sh
```