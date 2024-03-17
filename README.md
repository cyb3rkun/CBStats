# [Forgejo / Gitea Stats Visualization](https://codeberg.org/Tuxilio/forgejo-stats/)

[![status-badge](https://ci.codeberg.org/api/badges/13152/status.svg)](https://ci.codeberg.org/repos/13152)
[![license badge](https://img.shields.io/badge/License-GPL_v3-blue)](LICENSE)
[![Stars](https://img.shields.io/gitea/stars/Tuxilio/forgejo-stats?gitea_url=https%3A%2F%2Fcodeberg.org%2F)](https://codeberg.org/Tuxilio/forgejo-stats/stars)
[![Issues](https://img.shields.io/gitea/issues/open/Tuxilio/forgejo-stats?gitea_url=https%3A%2F%2Fcodeberg.org%2F)](https://codeberg.org/Tuxilio/forgejo-stats/issues)

<a href="https://codeberg.org/Tuxilio/forgejo-stats">
<img src="generated/overview.svg#gh-dark-mode-only"/>
<img src="generated/languages.svg#gh-dark-mode-only"/>
<br>
<img src="generated/overview.svg#gh-light-mode-only"/>
<img src="generated/languages.svg#gh-light-mode-only"/>
</a>

Generate visualizations of Forgejo / Gitea user and repository statistics with Python - e.g. using Forgejo / Gitea Actions. Visualizations can include data for private repositories.

You can choose between light and dark mode.

## Background

When someone views a profile, it is often because they are curious about a user's open source projects and contributions. Unfortunately, that user's stars, forks, and pinned repositories do not necessarily reflect the contributions they make.

This project aims to collect a variety of profile and repository statistics using the Forgejo / Gitea API. It then generates images that can be displayed in repository READMEs, or in a user's [Profile README](https://forgejo.org/docs/latest/user/profile/).

There are many GitHub statistics visualizations for GitHub. But also at Forgejo or Gitea some are interested in the number of stars of a user, the most used programming languages or the changed lines.

This project is still under development, but it's a good start. It is already possible to create simple visualizations.

This project uses [GitHub stats](https://github.com/jstrieb/github-stats) by [Jacob Strieb](https://github.com/jstrieb) (licensed under GPL 3.0 or later) as base and uses the [Language Colors](https://github.com/ozh/github-colors) by [OZH](https://github.com/ozh) (licensed under WTFPL) for the language color visualizations.

Since the project runs on Forgejo / Gitea Actions, no server is required to regularly regenerate the images with updated statistics. Likewise, since the user runs the analysis code themselves via Forgejo / Gitea Actions, they can use their access token to collect statistics on private repositories that an external service would be unable to access.

## Installation
### Using the CI
<!-- TODO: Add details and screenshots -->

1. Create a personal access token using the instructions [here](https://docs.codeberg.org/advanced/access-token/). Personal access token must have permissions: `Read - repository` and `Read - user`. Copy the access token when it is generated – if you lose it, you will have to
   regenerate the token.
<!-- TODO: Add explaination -->
   <!--
2. Create a copy of this repository by clicking
   [here](https://github.com/jstrieb/github-stats/generate). Note: this is
   **not** the same as forking a copy because it copies everything fresh,
   without the huge commit history. 
3. Go to the "Secrets" page of your copy of the repository. If this is the
   README of your copy, click [this link](../../settings/secrets/actions) to go
   to the "Secrets" page. Otherwise, go to the "Settings" tab of the
   newly-created repository and go to the "Secrets" page (bottom left).
4. Create a new secret with the name `ACCESS_TOKEN` and paste the copied
   personal access token as the value.
5. It is possible to change the type of statistics reported by adding other
   repository secrets. 
   - To ignore certain repos, add them (in owner/name format e.g.,
     `jstrieb/github-stats`) separated by commas to a new secret—created as
     before—called `EXCLUDED`.
   - To ignore certain languages, add them (separated by commas) to a new
     secret called `EXCLUDED_LANGS`. For example, to exclude HTML and TeX you
     could set the value to `html,tex`.
   - To show statistics only for "owned" repositories and not forks with
     contributions, add an environment variable (under the `env` header in the
     [main
     workflow](https://github.com/jstrieb/github-stats/blob/master/.github/workflows/main.yml))
     called `EXCLUDE_FORKED_REPOS` with a value of `true`.
   - These other values are added as secrets by default to prevent leaking
     information about private repositories. If you're not worried about that,
     you can change the values directly [in the Actions workflow
     itself](https://github.com/jstrieb/github-stats/blob/05de1314b870febd44d19ad2f55d5e59d83f5857/.github/workflows/main.yml#L48-L53).
6. Go to the [Actions
   Page](../../actions?query=workflow%3A"Generate+Stats+Images") and press "Run
   Workflow" on the right side of the screen to generate images for the first
   time. 
   - The images will be automatically regenerated every 24 hours, but they can
     be regenerated manually by running the workflow this way.
7. Take a look at the images that have been created in the
   [`generated`](generated) folder.
8. To add your statistics to your GitHub Profile README, copy and paste the
   following lines of code into your markdown content. Change the `username`
   value to your GitHub username.
   ```md
   ![](https://raw.githubusercontent.com/username/github-stats/master/generated/overview.svg#gh-dark-mode-only)
   ![](https://raw.githubusercontent.com/username/github-stats/master/generated/overview.svg#gh-light-mode-only)
   ```
   ```md
   ![](https://raw.githubusercontent.com/username/github-stats/master/generated/languages.svg#gh-dark-mode-only)
   ![](https://raw.githubusercontent.com/username/github-stats/master/generated/languages.svg#gh-light-mode-only)
   ```
   -->
9. Link back to this repository so that others can generate their own
   statistics images.
10. Star this repo if you like it!

### Running yourself
First, install requests:

     pip install requirements.txt

Now you can run the main program:

     python3 main.py

# Support the Project

There are a few things you can do to support the project:

- Star the repository (and follow me on Codeberg for more)
- Report any bugs, glitches, or errors that you find

These things motivate me to to keep sharing what I build, and they provide validation that my work is appreciated! They also help me improve the project. Thanks in advance!

# Related Projects

- Inspired by [GitHub stats](https://github.com/jstrieb/github-stats) by [Jacob Strieb](https://github.com/jstrieb)
- Inspired by a desire to improve upon [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats)
- Makes use of [GitHub Octicons](https://primer.style/octicons/)

> **Info** Wondering why there are so few commits?<br>
I first migrated Jacob Strie's project from GitHub to fork it and have it as a base but then the commit history was such large - so I deleted the repo and uploaded just the files to have an empty commit history.
