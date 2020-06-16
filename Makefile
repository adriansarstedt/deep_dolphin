PROJECT := deep_dolphin

setup:
	@echo
	@echo "In order to import deep_dolphin locally its project directory"
	@echo "must be added to your python path. To do this, please execute"
	@echo "the following command in your local CLI:"
	@echo "export PYTHONPATH=$$PYTHONPATH:$$PWD"
	@echo

install_dependencies:
	pip install -r dependencies.txt

test:
	# must include the -P tag to enforce no-path-adjustment
	# https://stackoverflow.com/questions/16200333/import-errors-when-running-nosetests-that-i-cant-reproduce-outside-of-nose/26584815#26584815
	# able to add multiple test directories as shown below
	# $ nosetests tests/contouring tests/server
	nosetests -P tests/contouring tests/helpers tests/dicom
