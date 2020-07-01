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

TEST_DIRECTORIES = tests/contouring tests/helpers tests/dicom tests/nii

test:
	# must include the -P tag to enforce no-path-adjustment
	nosetests -P $(TEST_DIRECTORIES)

test_with_coverage_report:
	nosetests -P $(TEST_DIRECTORIES) --with-coverage
	codecov