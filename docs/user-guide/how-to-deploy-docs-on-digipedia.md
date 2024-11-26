---
title: How-to-deploy-docs-on-digipedia
author: Jon Steinar Folstad
date: 2024-11-06
---

# How-to-Guide - Deployment to Digipedia and Github Pages
_Last updated November 1st, 2024 | Author: Jon Steinar Folstad_

## Prerequisites

Ensure you have read the [How-to-Guide - MkDocs Documentation](how-to-setup-mkdocs.md), and your project follows this file structure:

```
your_project/
└── docs/
    ├── build/                     # Output directory where HTML files are generated
    │   ├── html/                  # HTML files go here after building
    │   └── doctrees/              # Stores intermediary files for fast rebuilds
    │
    ├── source/                    # Source files directory
    │   ├── _static/               # Custom static files (CSS, JS, images, etc.)
    │   ├── _templates/            # Custom templates (e.g., for modifying HTML layout)
    │   ├── conf.py                # Main configuration file for Sphinx
    │   └── index.rst              # Main document (typically the homepage of your docs)
    │
    ├── Makefile                   # Build file for Unix/Linux
    └── make.bat                   # Build file for Windows
```

If your file structure deviates from the above, you may need to modify the workflow files located in `.github/workflows/` to ensure successful documentation generation deployment. Adjust the paths in the workflow to match your project structure if needed.

## Generate SSH deploy key in terminal

To generate an SSH deploy key specifically for pushing from one repository to another repository, follow these steps:

1. Generate a New SSH Key Pair

Open a terminal on your Linux machine and run the following command to generate a new SSH key pair:

```bash
ssh-keygen -t rsa -b 4096 -f ./id_rsa
```

When prompted to "Enter a file in which to save the key," you can press Enter to accept the default location or specify a different path.
When prompted for a passphrase, you can either enter a secure passphrase or leave it empty for no passphrase.

To add any comment to ssh pair use flag `-c <add_your_comment>`

2. Add the private key to Source repository (your project repository) and Public Key to the Target Repository [dig-handbook-mkdocs](https://github.com/AkerBP/dig-handbook-mkdocs/)

Copy the private key to your clipboard:

```bash
cat ~/.ssh/id_rsa
```

Copy the public key to your clipboard:

```bash
cat ~/.ssh/id_rsa.pub
```

Follow these steps to add the Private Key to your project repository

1. Navigate to your GitHub repository where the workflow is defined.
2. Click on the "Settings" tab.
3. In the left sidebar, click on "Secrets and variables" and then "Actions."
4. Click on "New repository secret."
5. Name the secret SSH_DEPLOY_KEY_DIGIPEDIA.
6. Paste the contents of your private key into the "Value" field.
7. Click "Add secret."

> **Note** Your ssh private key begines with '-----BEGIN OPENSSH PRIVATE KEY-----', and it ends with '-----END OPENSSH PRIVATE KEY-----'.

Then, add the public key to the target repository:

1. Navigate to the target repository on GitHub.
2. Click on the "Settings" tab.
3. In the left sidebar, click on "Deploy keys."
4. Click on "Add deploy key."
5. Give your key a title, paste the public key into the "Key" field, and check the "Allow write access" box if necessary.
6. Click "Add key."

> **Note** Your ssh public key begins with 'ssh-rsa', 'ecdsa-sha2-nistp256', 'ecdsa-sha2-nistp384', 'ecdsa-sha2-nistp521', 'ssh-ed25519', 'sk-ecdsa-sha2-nistp256@openssh.com', or 'sk-ssh-ed25519@openssh.com'.

## Add Documentation to DigiPedia and GitHub Pages

Distribute your project documentation to **DigiPedia** and **GitHub Pages** with these steps.

### Deploy Docs to [DIGiPedia](https://studious-succotash-69n7n96.pages.github.io/)

1. **Add Workflow**
   Copy the [`gh-copy-html-to-repo.yaml`](https://github.com/AkerBP/expres-copilot-data/blob/docs/document-project-using-sphinx/.github/workflows/gh-copy-html-to-repo.yaml) file to `.github/workflows/` in your project root.

2. **Contact for Details**
   Email jon.steinar.folstad@akerbp.com from Data Science & Analytics to obtain DigiPedia destination details.

3. **Configure Workflow**
   In `gh-copy-html-to-repo.yaml`, modify `<BU>` with the destination information provided, and `<repository-name>` with the name of your repository. Also, modify `user-email`, `user-name` and `commit-message` to reflect your user information and repository changes.

   ```yaml
   printf "nav:\n  - README.md\n  - docs: ./code/<BU>/<repository-name>/docs/" > docs/build/publish/.pages

   source-directory: docs/build/publish
   destination-github-username: "AkerBP"
   destination-repository-name: "dig-handbook-mkdocs"
   target-branch: git-docs
   target-directory: docs/code/<BU>/$\{\{ github.event.repository.name \}\}
   user-email: <your user email adress>
   user-name: <your github user-name>
   commit-message: "[GHA] Update <repository name> docs html files."
   ```

4. **Check Deployment**

Go to the [Digipedia GitHub repository](https://github.com/AkerBP/dig-handbook-mkdocs/tree/git-docs/docs/code) to verify that your files are present in the `docs/code` directory.

If the deployment was successful, you can view your documentation on [DIGipedia Pages](https://studious-succotash-69n7n96.pages.github.io/).

> Note: This DIGpedia page is a copy of the original DIGpedia page. You would be notified when these two pages would merge together.

### Deploy docs to Github Pages

1. Add and configure Workflow
Modify the workflow file with necessary information for GitHub Pages deployment.

Add [`gh-pages-deploy-sphinx.yaml`](https://github.com/AkerBP/expres-copilot-data/blob/docs/document-project-using-sphinx/.github/workflows/gh-pages-deploy-sphinx.yaml)` to the folder .github/workflows/ on project root.

2. Check Deployment
Go to your repository's Settings tab, select Pages from the sidebar, and visit the provided URL to confirm your site is live.

## References
- [Documentation destination](https://github.com/AkerBP/dig-handbook-mkdocs)
- [Deploy to DIGipedia](https://github.com/AkerBP/expres-copilot-data/blob/docs/document-project-using-sphinx/.github/workflows/gh-copy-html-to-repo.yaml)
- [Deploy to Github Pages](https://github.com/AkerBP/expres-copilot-data/blob/docs/document-project-using-sphinx/.github/workflows/gh-pages-deploy-sphinx.yaml)
