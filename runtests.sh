#!/bin/bash

if [ -f "test_auction.py" ]; then
	TESTMODULE="test_auction.py"
elif [ -f "auction_test.py" ]; then
	TESTMODULE="auction_test.py"
else
	echo "No test file test_auction.py or auction_test.py"
	exit 9
fi

# arrays to record results. Elements are appended in runtests()
expect=("")
actual=("")

drawline( ) {
    echo "----------------------------------------------------------------------"
}

runtests( ) {
	for testcase in 1 2 3 4 5 6 7 8; do
        echo ""
        drawline
        # append new element to expect. All testcases should fail except 1.
        expect+=("FAIL")
		case $testcase in
    	1)
			echo "AUCTION CODE 1: All methods work according to specification. Your tests should PASS."
			# this case should pass all tests
			expect[1]="OK"
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
		# record status
		if [ $? -eq 0 ]; then
			actual+=("OK")
		else
			actual+=("FAIL")
		fi
		# wait til user presses enter
		# read input
	done
}

showresults() {
    drawline
    echo "RESULTS of 8 Auction Tests"
    drawline
    echo "OK=all tests pass, FAIL=some tests fail"
    echo ""
    echo "Auction#  Expect  Actual"
    failures=0
	for testcase in 1 2 3 4 5 6 7 8; do
        printf "%5d      %-4s     %s\n" ${testcase} ${expect[$testcase]} ${actual[$testcase]}
        if [ ${expect[$testcase]} != ${actual[$testcase]} ]; then
			failures=$(($failures+1))
		fi
	done
    correct=$((8-$failures))
	echo "$correct Correct  $failures Incorrect"
    exit $failures
}

runtests
showresults
