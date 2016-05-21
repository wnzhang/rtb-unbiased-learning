campaigns="1458 2259 2261 2821 2997 3358 3386 3427 3476"
folder=../../make-ipinyou-data
resultsfolder=../results

if [ ! -d $resultsfolder ]; then
  mkdir $resultsfolder
fi

for campaign in $campaigns; do
    echo $campaign
    # run logistc regression
    #python ../python/lryzx.py $folder/$campaign/train.yzx.txt $folder/$campaign/test.yzx.txt

    #yzp train dataset p for ptcr
    #python ../python/lryzp.py $folder/$campaign/train.yzx.txt $folder/$campaign/train.yzp.txt $folder/$campaign/test.yzx.txt $folder/$campaign/test.yzp.txt


    # mcpc bidding for train yzp dataset
    #python ../python/mcpc-bid.py $folder/$campaign/train.yzp.txt $folder/$campaign/train.win.yzp.txt
    
    # run real-time bidding test
    # b1
    python ../python/rtb-test.py $folder/$campaign/train.win.yzp.txt $folder/$campaign/test.yzp.txt $resultsfolder/b1.train.results.$campaign.txt $resultsfolder/b1.test.results.$campaign.txt
    # b3
    python ../python/rtb-test.py $folder/$campaign/train.yzp.txt $folder/$campaign/test.yzp.txt $resultsfolder/b3.train.results.$campaign.txt $resultsfolder/b3.test.results.$campaign.txt
    # check the best perf
    #python ../python/check-best-perf.py $resultsfolder/rtb.results.$campaign.tsv
done
