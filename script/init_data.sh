campaigns="2997"
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
    python ../python/lryzp.py $folder/$campaign/train.yzx.txt $folder/$campaign/train.yzp.txt $folder/$campaign/test.yzx.txt $folder/$campaign/test.yzp.txt


    # mcpc bidding for train yzp dataset
    python ../python/mcpc-bid.py $folder/$campaign/train.yzp.txt $folder/$campaign/train.win.yzp.txt
    
    # run real-time bidding test
    #python ../python/mcpc-bid.py $folder/$campaign/train.yzx.txt $folder/$campaign/test.yzx.txt $folder/$campaign/test.yzx.txt.lr.pred $resultsfolder/rtb.results.$campaign.tsv
    
    # check the best perf
    #python ../python/check-best-perf.py $resultsfolder/rtb.results.$campaign.tsv
done
