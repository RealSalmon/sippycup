# The name of the lambda function to use when deploying
DEPLOY_NAME=sippycup-demo

# The name of the AWS CLI profile to use when deploying
DEPLOY_PROFILE=sippycup-demo

# The name of the main file or directory. It is expected that this will be in
# the root directory
FUNCTION_FILE = lambda_function.py

# The name of the folder that contains the virtual environment for this project
VIRTUALENV = venv

# Additional files/folders in the root directory that should be included
# Note that the relative path of these files will be preserved, unlike
# PACKAGES, which could create a conflict. PACKAGES will take precedence
# since it is executed last
INCLUDES = "sippycup"

# Should packages in lib/python2.7/site-packages be packaged?
# If the project does not require additional packages and/or
# none have been installed then set this to false
PACKAGES = true

# Pattern in addition to BASE_EXCLUDES that should be excluded
EXCLUDES = ""

# Standard exclusions
# These may need to be adjusted based on the nature of the project
# boto3 and dependencies are included in this exclusion list
BASE_EXCLUDES = "_markerlib/*" "easy_install.py*" "pip/*" "pip-*" \
                "pkg_resources/*" "wheel/*" "setuptools/*" "*dist-info*" \
                "*.pyc" \
                "boto3/*" "docutils/*" "jmespath/*" "python-dateutil/*" \
                "six.py" "s3transfer/*" "botocore/*" "futures/*" \
                "tox/*" "virtualenv_support/*" "py/*" "pluggy.py" \
                "virtualenv.py"


SHELL := /bin/bash

PACKAGE_NAME=$$(basename $(FUNCTION_FILE) .py).zip

package:
	rm -f $(PACKAGE_NAME)
	zip $(PACKAGE_NAME) -r $(FUNCTION_FILE) $(INCLUDES)
ifeq ($(PACKAGES), true)
		pushd $(VIRTUALENV)/lib/python2.7/site-packages/;\
		zip $$(dirs -l -0)/$(PACKAGE_NAME) -r ./ -x $(BASE_EXCLUDES) $(EXCLUDES)
endif

list-package: package
	unzip -l $(PACKAGE_NAME)

deploy: package
	aws lambda update-function-code \
		--profile $(DEPLOY_PROFILE) \
		--zip-file fileb://$(PACKAGE_NAME) \
		--function-name $(DEPLOY_NAME)
