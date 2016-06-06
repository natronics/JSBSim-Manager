all: analysis

analysis: analysis.ipynb
	jupyter nbconvert --execute --to=markdown --template="nb-markdown.tpl" $^
	mv analysis.md README.markdown

sim:
	./run.py

clean:
	rm -rf thread_*
	rm -f data/*.csv
