#!/bin/bash

function build() {
    charm=$1
    pushd $charm-operator/
    charmcraft clean
    charmcraft build
    mv ${charm}_ubuntu-20.04-amd64.charm $charm.charm
    popd
}

pushd charms/kamailio-bundle
    charms="kamailio-k8s sipp-k8s"
    for charm in $charms; do
        build $charm
        wait
    
    done

popd
