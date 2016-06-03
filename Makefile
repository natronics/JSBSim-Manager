README.markdown: rocket.ipynb
	jupyter nbconvert --execute --to=markdown --template="nb-markdown.tpl" $^
	mv rocket.md README.markdown

clean:
	rm -rf aircraft
	rm -rf engine
