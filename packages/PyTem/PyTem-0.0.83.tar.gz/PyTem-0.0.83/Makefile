
help:
	@echo "Targets:"
	@echo "   clean           Delete build/test artifacts"
	@echo "   demo1           Test expandFile API and include_template."
	@echo "   demo2           Test expandString."
	@echo "   demo3           Test command line expansion of two files."
	@echo "   demo4           Test some other expanString cases."
	@echo
	@echo "   gitcommit    		remember to commit to git:"
	@echo "            					git status"
	@echo "            					git add './*'"
	@echo "            					git commit -a -m \"latest changes\""
	@echo "            					git push"
	@echo
	@echo "   local_install   Copy ./pytem.py to ../../lib/python3.5/site-packages/pytem.py"
	@echo
	@echo " I haven't been able to get this stuff to work since they changed the API"
	@echo " to pypi...;  but see:"
	@echo "				http://peterdowns.com/posts/first-time-with-pypi.html"
	@echo "	and"
	@echo "				https://packaging.python.org/tutorials/distributing-packages/#uploading-your-project-to-pypi"
	@echo
	@echo "   sdist           Build a pypi distribution. NOTE: Update version in setup.py!"
	@echo "   register_sdist  Register (1st time) and upload (all times) with pypi"
	@echo "        In addition to 'sdict' and 'register_sdict' to release to pypi,"
	@echo

clean:
	@rm -f *.out
	@rm -f *.tm.py
	@rm -f README.html README.txt
	@rm -rf __pycache__

demo1:
	@python pytem_demo1.py

demo2:
	@python pytem_demo2.py

demo3:
	@python pytem.py -d 0x0100 -o pytem_demo3.out -p pytem_demo3.tm pytem_demo3a.tm

demo3A: 
	@python pytem.py -d 0x0100 -o pytem_demo3A.out -p pytem_demo3.tm - <pytem_demo3a.tm

demo4:
	@python pytem_demo4.py

demo5: 
	@#./pytem.py pytem_demo5a.tm - <pytem_demo5b.tm >pytem_demo5.txt
	@./pytem.py pytem_demo5a.tm pytem_demo5b.tm >pytem_demo5.txt

sdist: clean
	@pandoc -s README.md -o README.txt
	@python setup.py check
	@python setup.py sdist --formats=zip

#Initial registration with pypi:
register_sdist:
	python setup.py register sdist upload


# Local install the pytem.py module
local_install:
	cp ./pytem.py  ../../lib/python3.5/site-packages/pytem.py
	chmod +x ../../lib/python3.5/site-packages/pytem.py
	cp ./pytem.py  ~/.pyenv/versions/3.5.1/lib/python3.5/site-packages/pytem.py
	chmod +x  ~/.pyenv/versions/3.5.1/lib/python3.5/site-packages/pytem.py
	ln -sf ~/.pyenv/versions/3.5.1/lib/python3.5/site-packages/pytem.py ~/bin/pytem


