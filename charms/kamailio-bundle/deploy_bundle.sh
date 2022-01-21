#!/bin/bash

pushd charms/kamailio-bundle/
juju deploy ./bundle.yaml --trust
popd