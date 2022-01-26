#!/bin/bash

pushd charms/kamailio-bundle/
  git clone  -b main https://github.com/davigar15/charm-kamailio.git \
  && cp -r charm-kamailio/* kamailio-operator/ && rm -rf charm-kamailio;
  git clone  https://github.com/davigar15/sipp-operator.git  \
  && cp -r sipp-operator/*  sipp-k8s-operator/ && rm -rf sipp-operator;

popd
