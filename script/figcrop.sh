files=../tex/figs/*winprob.pdf
for file in $files; do
pdfcrop $file $file
done

files=../tex/figs/*auc-perf.pdf
for file in $files; do
pdfcrop $file $file
done

files=../tex/figs/*improvement.pdf
for file in $files; do
pdfcrop $file $file
done

