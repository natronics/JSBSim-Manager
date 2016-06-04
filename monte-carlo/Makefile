README.markdown: monte-carlo.ipynb
	jupyter nbconvert --execute --config=convert_config.py --to=markdown --template="nb-markdown.tpl" $^
	mv monte-carlo.md README.markdown

clean:
	rm -rf aircraft
	rm -rf engine
	rm -f output_file.xml
	rm -f *.csv
