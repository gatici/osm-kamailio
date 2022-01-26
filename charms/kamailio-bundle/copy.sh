#!/bin/bash

pushd charms/kamailio-bundle/
path=`pwd`
for i in kamailio-k8s sipp-k8s
do
    cp  $i'-operator/'$i'.charm'  $path/../../kamailio_cnf/juju-bundles/$i'-operator/'
done
popd
