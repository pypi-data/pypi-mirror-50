.. image:: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-mr/badges/master/pipeline.svg
   :target: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-mr
   :alt: Pipeline Status

.. image:: https://img.shields.io/pypi/l/gitlab-auto-mr.svg
   :target: https://pypi.org/project/gitlab-auto-mr/
   :alt: PyPI Project License

.. image:: https://img.shields.io/pypi/v/gitlab-auto-mr.svg
   :target: https://pypi.org/project/gitlab-auto-mr/
   :alt: PyPI Project Version

.. image:: https://readthedocs.org/projects/gitlab-auto-mr/badge/?version=latest
   :target: https://gitlab-auto-mr.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

GitLab Auto MR
==============

This is a simple Python script that allows you create MR in GitLab automatically. It is intended to be used in CI/CD
as a Docker image. However you can use it as a separate Python library if you would like.
An example CI using this can be found `here <https://gitlab.com/stegappasaurus/stegappasaurus-app/blob/master/.gitlab-ci.yml>`_.

It is based on the script and idea of `Riccardo Padovani <https://rpadovani.com>`_,
which he introduced with his blog post
`How to automatically create new MR on Gitlab with Gitlab CI <https://rpadovani.com/open-mr-gitlab-ci>`_.

This package was intended to be used by GitLab CI hence using environments provided by the GitLab CI. You can however
use it as a CLI tool if you would like.

Usage
-----

First you need to create a personal access token,
`more information here <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_.
With the scope ``api``, so it can create the MR using your API.

.. code-block:: bash

    pip install gitlab-auto-mr
    gitlab_auto_mr --help

  Usage: gitlab_auto_mr [OPTIONS]

    Gitlab Auto MR Tool.

  Options:
    --private-token TEXT      Private GITLAB token, used to authenticate when
                              calling the MR API.  [required]
    --source-branch TEXT      The source branch to merge into.  [required]
    --project-id INTEGER      The project ID on GitLab to create the MR for.
                              [required]
    --project-url TEXT        The project URL on GitLab to create the MR for.
                              [required]
    --user-id INTEGER         The GitLab user ID to assign the created MR to.
                              [required]
    -t, --target-branch TEXT  The target branch to merge onto.
    -c, --commit-prefix TEXT  Prefix for the MR title i.e. WIP.
    -r, --remove-branch       Set to True if you want the source branch to be
                              removed after MR.
    -s, --squash-commits      Set to True if you want commits to be squashed.
    -d, --description TEXT    Path to file to use as the description for the MR.
    --use-issue-name          If set to True will use information from issue in
                              branch name, must be in the form #issue-number,
                              i.e feature/#6.
    --allow-collaboration     If set to True allow, commits from members who can
                              merge to the target branch.
    --help                    Show this message and exit.


.. code-block:: bash

    gitlab_auto_mr --private-token $(private_token) --source-branch feature/test --project-id 5 \
                    --project-url https://gitlab.com/stegappasaurus/stegappasaurus-app --user-id 5

GitLab CI
*********

``GITLAB_PRIVATE_TOKEN`` Set a secret variable in your GitLab project with your private token. Name it
GITLAB_PRIVATE_TOKEN (``CI/CD > Environment Variables``). This is necessary to raise the Merge Request on your behalf.
More information `click here <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_.
An example CI using this can be `found here <https://gitlab.com/stegappasaurus/stegappasaurus-app/blob/master/.gitlab-ci.yml>`_.

Add the following to your ``.gitlab-ci.yml`` file:

.. code-block:: yaml

    stages:
      - open

    open_merge_request:
      image: registry.gitlab.com/gitlab-automation-toolkit/gitlab-auto-mr
      before_script: [] # We do not need any setup work, let's remove the global one (if any)
      variables:
        GIT_STRATEGY: none # We do not need a clone of the GIT repository to create a Merge Request
      stage: open
      only:
        - /^feature\/*/ # We have a very strict naming convention
      script:
        - gitlab_auto_mr

Changelog
=========

You can find the `changelog here <https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-mr/blob/master/CHANGELOG.md>`_.

Appendix
========

- Extra features: `Allsimon <https://gitlab.com/Allsimon/gitlab-auto-merge-request>`_
- Forked from: `Tobias L. Maier <https://gitlab.com/tmaier/gitlab-auto-merge-request>`_
- Script and idea: `Riccardo Padovani <https://rpadovani.com>`_
