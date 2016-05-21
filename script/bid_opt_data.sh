campaigns="2261"
#campaigns="1458 2259 2261 2821 2997 3358 3386 3427 3476 all"

for campaign in $campaigns; do
    echo $campaign

    python ../python/lr_wyzp.py $campaign
done
