#! /bin/sh

# IPOPT and MUMPS
if [ ! -d "lib/ipopt" ] && [ "$OPTALG_IPOPT" = true ]; then
    mkdir -p lib
    cd lib
    wget https://www.coin-or.org/download/source/Ipopt/Ipopt-3.12.8.zip
    unzip Ipopt-3.12.8.zip
    mv Ipopt-3.12.8 ipopt
    cd ipopt/ThirdParty/Mumps
    ./get.Mumps
    cd ../../
    ./configure
    make clean
    make uninstall
    make
    #make test
    make install
    cp lib/libipopt* ../../optalg/opt_solver/_ipopt
    cp lib/libcoinmumps* ../../optalg/lin_solver/_mumps
    cd ../../
fi

# CLP
if [ ! -d "lib/clp" ] && [ "$OPTALG_CLP" = true ]; then
    mkdir -p lib
    cd lib
    wget https://www.coin-or.org/download/source/Clp/Clp-1.16.11.zip 
    unzip Clp-1.16.11.zip
    mv Clp-1.16.11 clp
    cd clp
    ./configure
    make clean
    make uninstall
    #make test
    make install
    cp lib/libClp* ../../optalg/opt_solver/_clp
    cd ../../
fi