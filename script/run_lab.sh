campaigns="3476"
#campaigns="1458 2259 2261 2821 2997 3358 3386 3427 3476 all"
folder=../../make-ipinyou-data
resultsfolder=../results
aucrmse=../results/auc-rmse


if [ ! -d $resultsfolder ]; then
  mkdir $resultsfolder
fi

if [ ! -d $aucrmse ]; then
  mkdir $aucrmse
fi

for campaign in $campaigns; do
    echo $campaign

    #add w=1 to train.yzx.txt to get tsrain.wyzx.txt
    #python ../python/add_w_const.py $folder/$campaign/train.yzx.txt $folder/$campaign/train.wyzx.txt

    #segment train.wyzx.txt into 2 files:train.wyzx.base.txt and train.wyzx.bid.txt
    #python ../python/seg.py $folder/$campaign/train.wyzx.txt $folder/$campaign/train.wyzx.base.txt $folder/$campaign/train.wyzx.bid.txt

    #use train.wyzx.base.txt as train data to build lr_mcpc on train.wyzx.bid.txt
    #python ../python/lr_mcpc.py $folder/$campaign/train.wyzx.base.txt $folder/$campaign/train.wyzx.bid.txt $folder/$campaign/train.wyzx.imp.txt $folder/$campaign/train.wyb.imp.txt $folder/$campaign/train.wyb.lose.txt $folder/$campaign/train.wyzx.uimp.txt

    #combine win and lose datafile into one file: oyb, o is the boolean value of whether this is a win result or a lose result.  
    #python ../python/build_oyb.py $folder/$campaign/train.wyzx.imp.txt $folder/$campaign/train.wyb.lose.txt $folder/$campaign/train.bo.bid.sorted.txt

    #Kaplan–Meier estimator for bid landscape function
    #python ../python/kaplan_meier.py $folder/$campaign/train.bo.bid.sorted.txt $folder/$campaign/train.wyzx.imp.txt $folder/$campaign/train.wyb.imp.txt $folder/$campaign/train.wyzx.kimp.txt

    #AUC and RMSE performance on test.yzx.txt by train.wyzx.imp.txt, train.wyzx.uimp.txt and train.wyzx.bid.txt

    #python ../python/auc_rmse.py $folder/$campaign/train.wyzx.imp.txt $folder/$campaign/test.yzx.txt $aucrmse/test.aucRmse.imp.$campaign.txt $aucrmse/test.ar.rounds.imp.$campaign.txt

    #python ../python/auc_rmse.py $folder/$campaign/train.wyzx.uimp.txt $folder/$campaign/test.yzx.txt $aucrmse/test.aucRmse.uimp.$campaign.txt $aucrmse/test.ar.rounds.uimp.$campaign.txt

    #python ../python/auc_rmse.py $folder/$campaign/train.wyzx.kimp.txt $folder/$campaign/test.yzx.txt $aucrmse/test.aucRmse.kimp.$campaign.txt $aucrmse/test.ar.rounds.kimp.$campaign.txt

    #python ../python/auc_rmse.py $folder/$campaign/train.wyzx.bid.txt $folder/$campaign/test.yzx.txt $aucrmse/test.aucRmse.bid.$campaign.txt $aucrmse/test.ar.rounds.bid.$campaign.txt

    #build wyzp files where p is the ctr prediction based on base.txt and their own w
#    python ../python/build_wyzp.py $folder/$campaign/train.wyzx.base.txt $folder/$campaign/train.wyzx.imp.txt \
#        $folder/$campaign/train.wyzx.uimp.txt $folder/$campaign/train.wyzx.kimp.txt $folder/$campaign/train.wyzx.bid.txt \
#        $folder/$campaign/test.yzx.txt $folder/$campaign/train.wyzp.imp.txt $folder/$campaign/train.wyzp.uimp.txt \
#        $folder/$campaign/train.wyzp.kimp.txt $folder/$campaign/train.wyzp.bid.txt



    #train.yzp.base.txt
    #python ../python/lryzp.py $folder/$campaign/train.yzx.base.txt $folder/$campaign/train.yzp.base.txt

    # run real-time bidding test
    # b1
    python ../python/rtb_opt.py $folder/$campaign/train.win.yzp.txt $folder/$campaign/test.yzp.txt \
        $resultsfolder/rtb.train.results.$campaign.txt $resultsfolder/rtb.test.results.$campaign.txt
    # b3
    #python ../python/rtb_opt.py $folder/$campaign/train.yzp.txt $folder/$campaign/test.yzp.txt $resultsfolder/rtb.train.results.$campaign.txt $resultsfolder/rtb.test.results.$campaign.txt
    # check the best perf
    #python ../python/check-best-perf.py $resultsfolder/rtb.results.$campaign.tsv
done

#Get auc rmse results in one file 
#python ../python/auc_rmse_con.py $aucrmse $resultsfolder/auc.rmse.result.txt
