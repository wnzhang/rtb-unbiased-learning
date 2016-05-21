campaigns="all"
#campaigns="1458 2259 2261 2821 2997 3358 3386 3427 3476 all"
folder=../../make-ipinyou-data
resultsfolder=../results/bid-opt


if [ ! -d $resultsfolder ]; then
  mkdir $resultsfolder
fi

if [ ! -d $aucrmse ]; then
  mkdir $aucrmse
fi

for campaign in $campaigns; do
    echo $campaign

    # make bid opt data
    python ../python/lr_wyzp.py $campaign

    # run real-time bidding test
    # imp
    echo 'imp'
    python ../python/bid_opt.py $campaign imp

    # uimp
    echo 'uimp'
    python ../python/bid_opt.py $campaign uimp

    # kimp
    echo 'kimp'
    python ../python/bid_opt.py $campaign kimp

    # bid
    echo 'bid'
    python ../python/bid_opt.py $campaign bid

done

#python ../python/bid_opt_results_test.py

