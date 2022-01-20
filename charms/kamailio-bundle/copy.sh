path=`pwd`
for i in kamailio sipp-k8s
do
    cp  $i'-operator/'$i'.charm'  $path/../../kamailio_cnf/juju-bundles/$i'-operator/'
done
