#!/bin/bash

function build() {
    charm=$1
    cd $charm-operator/
    charmcraft clean
    charmcraft build
    mv ${charm}_ubuntu-20.04-amd64.charm $charm.charm
    cd ..
}

pushd charms/kamailio-bundle
    charms="kamailio sipp-k8s"
    for charm in $charms; do
        build $charm &
    done
    wait
popd