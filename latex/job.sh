# Remove all files
rm *.aux
rm *.log
rm *.pdf
rm *.dvi
rm *.png

cp template.tex output.tex
sed -i "s/\%/$1/g" output.tex
latex -interaction=nonstopmode -halt-on-error -jobname output output.tex output.dvi > log.log

if grep -q "!" log.log
then
	cp template.tex output.tex
	
	ERROR_COMMAND="\\\\scriptsize{\\\\colorbox{red}{\\\\color{white}{\\\\texttt{Invalid \\\\textrm{\\\\LaTeX}}}}}"

	sed -i "s/\%/$ERROR_COMMAND/g" output.tex
	latex -interaction=nonstopmode -halt-on-error -jobname output output.tex output.dvi > log.log
fi

dvipng -D 600 -bg 'Transparent' -fg 'White' output.dvi