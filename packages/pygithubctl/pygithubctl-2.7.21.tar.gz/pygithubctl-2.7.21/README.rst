pygithubctl
===========
|docs| |travis| |pypi| |coverage|

.. |docs| image:: http://img.shields.io/badge/Docs-latest-green.svg
.. |travis| image:: https://travis-ci.org/sarathkumarsivan/pygithubctl.svg?branch=master
.. |pypi| image:: https://img.shields.io/pypi/v/pygithubctl.svg
.. |coverage| image:: https://img.shields.io/badge/coverage-100%25-brightgreen

The GitHub command-line tool, pygithubctl, lets you download a specific file, folder or directory from a remote Git repository hosted on GitHub. You can also download an entire project from GitHub without version control data. Git operates on a whole-repository basis and if you have projects where finer-grained access is necessary, you can use submodules; each submodule is a separate Git project, and thus can be cloned individually. But if a project wasn't configured so from the beginning, you can make use of pygithubctl to download the file or folders you are really interested in.

Installation
------------

The pygithubctl can be installed via pip, the Python package manager. If pip isn’t already available on your system of Python, run the following commands to install it:
::

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py --user

Then install pygithubctl
::

    sudo pip install pygithubctl

Upgrade
-------
You can upgrade pygithubctl via pip, the Python package manager; issue the below command to perform the upgrade:
::

    sudo pip install pygithubctl --upgrade

Usage
-----
You can use pygithubctl by issuing the pygithubctl command. Below command downloads a single file named README.md from <repository-name>. The Git repository in this example is hosted in an enterprise GitHub server.
::

    pygithubctl fetch \
	   --hostname github.your.company.com \
   	   --auth-token <valid-token> \
   	   --repository <repository-name> \
   	   --branch master \
   	   --path README.md \
   	   --type file \
   	   --destination /tmp \
   	   --http-ssl-verify False

If you would like to download a file from public GitHub server, you can issue something like this. Please note that you should not specify the value of hostname in this case.
::

    pygithubctl fetch \
    	--auth-token <valid-token> \
    	--repository pygithubctl \
    	--owner sarathkumarsivan \
    	--branch master \
    	--path README.rst \
    	--type file \
    	--destination /tmp \
    	--http-ssl-verify True

Options
#######

**--hostname:**
  Hostname of your GitHub enterprise server. This option is required for accessing enterprise GitHub server. Please don't specify this option if you are planning to fetch files or directories from public GitHub repository; this option is only required for a Git repository hosted on an enterprise GitHub server. You can also specify the complete endpoint URL like this: https://{hostname}/api/v3 (Replace {hostname} placeholder with the actual hostname).

**--auth-token:**
  A personal access token to authenticate to GitHub server. This option is required if you are not using user credentials to authenticate the GitHub server.

**--username:**
  A valid username to authenticate to GitHub server. This option is required if you are not using a personal access token to authenticate the GitHub server.

**--password:**
  A valid password to authenticate to GitHub server. This option is required if you are not using a personal access token to authenticate the GitHub server.

**--owner:**
  Owner of the Git repository hosted through GitHub server. This option is required if you are downloading files and directories from public GitHub server.

**--repository:**
  Name of GitHub repository. Please make sure the value of repository is valid. This option is required.

**--branch:**
  Name of the branch; a pointer to a snapshot of your changes. This option is required if no tag is specified. The master branch would be considered as the default value if no branch or tag name is specified.

**--tag:**
  Name of tag; a version of a particular branch at a moment in time. This option is required if no branch is specified.

**--path:**
  A specific file or directory path in your repository to download. Make sure the value of this option should be a valid repository path. This option is required.

**--type:**
  Indicates whether the given path is a file or directory. You can specify the value of this option to f or file if the requested path is a file and d or dir for a directory. This option is required.

**--destination:**
  Destination directory path to download the file(s). Make sure the user who runs this command has write permission to download the file in the target directory. Present working directory would be considered as the default destination if this option is not specified while running the fetch command. This option is optional.

**--http-ssl-verify:**
  Boolean flag to enable or disable the SSL certificate verification. This is option is enabled by default and you should specify the value of http-ssl-verify to False if you want to disable SSL certificate verification. This option is optional.

**--verbose:**
  Enable debug level logging. You can enable verbose logging which exactly similar to the DEBUG level. If you see any unexpected behavior while issuing pygithubctl, enablling this option would be a good choice to identify the problem and trace the root cause. 

**--quiet:**
  Make little or no noise during the file transfer. During the normal execution of pygithubctl command, INFO level logs would be printed on the console; but if you provide --quiet option, the command would be executed silently.

Supports
--------
Tested on Python 2.7