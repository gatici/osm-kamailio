tar -czvf kamailio_cnf.tar.gz kamailio_cnf; osm vnfd-create kamailio_cnf.tar.gz;
tar -czvf kamailio_ns.tar.gz kamailio_ns; osm nsd-create kamailio_ns.tar.gz;
