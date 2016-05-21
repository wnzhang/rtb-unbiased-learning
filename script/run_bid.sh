campaigns="2997"
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
    #python ../python/lr_wyzp.py $campaign

    # run real-time bidding test
    # imp
    echo 'imp'
    python ../python/rtb_opt.py $folder/$campaign/train.wyzp.imp.txt $folder/$campaign/test.wyzp.txt $resultsfolder/bid.opt.results.imp.$campaign.train.txt $resultsfolder/bid.opt.results.imp.$campaign.test.txt

    # uimp
    echo 'uimp'
    python ../python/rtb_opt.py $folder/$campaign/train.wyzp.uimp.txt $folder/$campaign/test.wyzp.txt $resultsfolder/bid.opt.results.uimp.$campaign.train.txt $resultsfolder/bid.opt.results.uimp.$campaign.test.txt

    # kimp
    echo 'kimp'
    python ../python/rtb_opt.py $folder/$campaign/train.wyzp.kimp.txt $folder/$campaign/test.wyzp.txt $resultsfolder/bid.opt.results.kimp.$campaign.train.txt $resultsfolder/bid.opt.results.kimp.$campaign.test.txt

    # bid
    echo 'bid'
    python ../python/rtb_opt.py $folder/$campaign/train.wyzp.bid.txt $folder/$campaign/test.wyzp.txt $resultsfolder/bid.opt.results.bid.$campaign.train.txt $resultsfolder/bid.opt.results.bid.$campaign.test.txt

    # check the best perf
    #python ../python/check-best-perf.py $resultsfolder/rtb.results.$campaign.tsv
done

