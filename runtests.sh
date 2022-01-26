#!/bin/bash

TESTMODULE="test_auction.py"

drawline( ) {
    echo "----------------------------------------------------------------------"
}
runtests( ) {
	for testcase in 1 2 3 4 5 6 7 8; do
        echo ""
        drawline
		case $testcase in
    	1)
			echo "AUCTION CODE 1: All methods work according to specification. Your tests should PASS."
       		;;
		3)
			echo "AUCTION CODE 3: The auction is not rejecting some invalid bids."
			;;
		4 )
			echo "AUCTION CODE 4: The auction is not enforcing state correctly."
			;;
		5)
			echo "AUCTION CODE 5: Some problem is silently ignored. It should raise an exception."
			;;
		8)
			echo "AUCTION CODE 8: Two errors in Auction. Do your tests detect BOTH defects?"
			;;
    	*)
			echo "AUCTION CODE ${testcase}: Some error in auction. At least one test should FAIL."
			;;
		esac
        drawline
		export TESTCASE=$testcase
		python3 -m unittest -v $TESTMODULE
		# wait til user presses enter
		# read input
	done
}

runtests
