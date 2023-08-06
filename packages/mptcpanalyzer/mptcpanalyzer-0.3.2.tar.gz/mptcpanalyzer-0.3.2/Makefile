all:
	# disabled

doc:
	make -C docs html

# pypi accepts only rst
# see http://inre.dundeemt.com/2014-05-04/pypi-vs-readme-rst-a-tale-of-frustration-and-unnecessary-binding/
rst:
	cat README.md | pandoc -f markdown -t rst > README.rst


publish:
	# new system is setup.py sdist bdist_wheel
	python setup.py sdist bdist_wheel
	# twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/*
	twine upload --verbose dist/*
	echo "You probably want to also tag the version now:"
	echo "  git tag -a VERSION -m 'version X'"
	echo "  git push --tags"


transcripts:
	# https://cmd2.readthedocs.io/en/latest/freefeatures.html#script-files
	# ReGenerate tests
	tests/gen_transcripts.sh

tests:
	# Add -b to print standard output
	# python -munittest tests/cache_test.py -b
	tests/run_transcripts.sh
	# mptcpanalyzer --test tests/summary_server_2_filtered.txt
	# tests/run_tests.sh

develop:
	python setup.py develop --user

uninstall:
	python setup.py develop --user --uninstall

man:
	# wrong name for the program but can't override :/
	# see also rst2man in docutils*.deb
	help2man -n "mptcpanalyzer - a multipath tcp pcap analysis tool" -o docs/mptcpanalyzer.man mptcpanalyzer


.PHONY: doc tests gen_transcripts
