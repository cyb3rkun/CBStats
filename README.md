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

#### Using Woodpecker CI

1. Create a personal access token using the instructions [here](https://docs.codeberg.org/advanced/access-token/). Personal access token must have permissions: `Read - repository` and `Read - user`. Copy the access token when it is generated – if you lose it, you will have to regenerate the token.
2. Create a second personal access token with the permission `Read & write - repository`
3. Create a copy of this repository: Go to the [New repo](https://codeberg.org/repo/create/) site and select the template `Tuxilio/forgejo-stats`. Choose `Git content (Defalt branch)`. Note: this is **not** the same as forking a copy because it copies everything fresh without the huge commit history. 
4. If you use Codeberg, you'll have to request an account for Woodpecker CI [here](https://docs.codeberg.org/ci/).
5. Go to the CI page and select the repository. Go to settings (the gear on the top right corner) and select `Secrets`.
6. Add the following secrets:
	- `git_url` - e.g. `https://codeberg.org`
	- `user` - e.g. `Tuxilio`
	- `access_token` - Your access token generated in step 1
	- `commit_token` - Your access token generated in step 2
The tokens need the events `Cron` and if you want to run it manual `Manual`
6. Go to the repository page inside the CI and press "Run pipeline" on the top right corner to generate images for the first
   time.
     - We'll set up a cron job so the images will be automatically regenerated every 24 hours, but they can be regenerated manually by running the workflow this way.
7. Take a look at the images that have been created in the [`generated`](generated) folder. If all looks right, you're nearly done!
8. Set up a cron job: e.g `@daily` to run the workflow each day at midnight.
9. To add your statistics to your Profile README, copy and paste the following lines of code into your markdown content. Change the `username` value to your Forgejo / Gitea username.
   ```md
   <div align="center">
      <a href="https://codeberg.org/username/forgejo-stats">
      <img src="https://codeberg.org/username/forgejo-stats/media/branch/main/generated/overview.svg"/>
      <img src="https://codeberg.org/username/forgejo-stats/media/branch/main/generated/languages.svg"/>
      </a>
   </div>
   ```
10. Star this repo if you like it!

You're done! 🎉

If something has gone wrong, check everything again carefully. If it still doesn't work, please [open an issue](https://codeberg.org/Tuxilio/forgejo-stats/issues).

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

- Using [GitHub stats](https://github.com/jstrieb/github-stats) by [Jacob Strieb](https://github.com/jstrieb) as a base
- Inspired by a desire to improve upon [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats)
- Makes use of [GitHub Octicons](https://primer.style/octicons/)
