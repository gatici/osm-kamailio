# Kamailio Operators
#### https://www.kamailio.org/w/
#### Kamailio® (successor of former OpenSER and SER) is an Open Source SIP Server released under GPLv2+, able to handle thousands of call setups per second. 
#### Kamailio can be used to build large platforms for VoIP and realtime communications – presence, WebRTC, Instant messaging and other applications.

# Deploy the Charms with Juju
This process could be done after charms are cloned and built according to main guide.

## Prepare environment

```bash
juju add-model kamailio
```

## Deploy with Juju


Deploy bundle:

```bash
./deploy_bundle.sh
```
