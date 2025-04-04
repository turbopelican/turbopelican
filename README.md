<div align="center"><img width="400" alt="turbopelican logo" src="https://raw.githubusercontent.com/turbopelican/turbopelican/refs/heads/main/assets/logo.svg"/></div>

# turbopelican

[![turbopelican](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/turbopelican/turbopelican/refs/heads/main/assets/badge/v1.json)](https://github.com/turbopelican/turbopelican)

An uber-quick tool to create a Pelican static-site and deploy it to GitHub
Pages.

## Explanation

GitHub lets you host static websites at your own subdomain. If your GitHub
username is **mrjohndoe**, you can host a website at
`https://mrjohndoe.github.io`. The same applies for organizations. If your
GitHub organization is called **MySpecialOrg**, you can host a website at
`https://myspecialorg.github.io`.

`turbopelican` is a tool which swiftly creates a static website to deploy at
your subdomain. Any developer with a GitHub account and `uv` installed
(**[see here](https://docs.astral.sh/uv/getting-started/installation/)**) can
deploy a website in minutes.

## Usage

Before you run `turbopelican`, create a new repository where you will keep the
source for your website.

> ℹ️  **_NOTE:_**  Make sure that the site-url uses the GitHub repository's name.
For example, if you want the website to be `https://johndoe.github.io`, your
GitHub repository will need to be called `johndoe.github.io`.

![Create your repository on GitHub](https://raw.githubusercontent.com/turbopelican/turbopelican/refs/heads/main/assets/docs/create-repo.png)

After your repository is created, copy the git repository URL. You'll need it
later.

![Obtain your repository URL](https://raw.githubusercontent.com/turbopelican/turbopelican/refs/heads/main/assets/docs/get-repo-reference.png)

Then enter your settings for your repository, and under "**Code and
automation**" click "**Pages**". The section "**Build and deployment**" allows
you to choose a source. Chose "**GitHub actions**".

![Configure site publication](https://raw.githubusercontent.com/turbopelican/turbopelican/refs/heads/main/assets/docs/github-actions-settings.png)

Next, you need to run `turbopelican`. Users are recommended to run
`turbopelican` using `uvx`:

```sh
$ uvx turbopelican init turbopelican.github.io
Who is the website author? [Ilya Simpson]
What is the name of the website? [turbopelican.github.io] Time to Clock Back
What timezone will your website use? [Pacific/Auckland]
What language will your website use? [en]
What is your website URL? [https://turbopelican.github.io]
Initialized empty Git repository in /home/elliot/projects/turbopelican.github.io/.git/
Using CPython 3.11.11
Creating virtual environment at: .venv
Resolved 23 packages in 0.66ms
Installed 21 packages in 13ms
 + anyio==4.9.0
 + blinker==1.9.0
 + docutils==0.21.2
 + feedgenerator==2.1.0
 + idna==3.10
 + jinja2==3.1.6
 + markdown==3.7
 + markdown-it-py==3.0.0
 + markupsafe==3.0.2
 + mdurl==0.1.2
 + ordered-set==4.1.0
 + pelican==4.11.0
 + pygments==2.18.0
 + python-dateutil==2.9.0.post0
 + pytz==2025.1
 + rich==13.9.4
 + six==1.17.0
 + sniffio==1.3.1
 + typing-extensions==4.12.2
 + unidecode==1.3.8
 + watchfiles==1.0.4
```

You can use the defaults, or choose your own values. In the example above, I
have decided to give the website a non-default name, but I have left the other
settings. `turbopelican` then creates a new repository `mypersonalsite`, with
everything ready to push to GitHub.

> ℹ️  **_NOTE:_**  Make sure that the site-url uses the GitHub repository's name.
For example, if you want the website to be `https://johndoe.github.io`, your
GitHub repository will need to be called `johndoe.github.io`.

You will then need to push your code to GitHub:

```sh
cd turbopelican.github.io
git add .
git commit -q -m "Initial commit."
git remote add origin git@github.com:turbopelican/turbopelican.github.io.git # Use your own git repo reference
git push -q --set-upstream origin main
```

Now look at your repository on GitHub. You should be able to see the
repository:

![View new repository](https://raw.githubusercontent.com/turbopelican/turbopelican/refs/heads/main/assets/docs/view-new-repo.png)

If you navigate back to the settings for GitHub Pages, you should see a
message informing you that your website is already live.

> ℹ️  **_NOTE:_** It may take a minute for this prompt to appear, because
GitHub Actions must first deploy your website.

![Site is live](https://raw.githubusercontent.com/turbopelican/turbopelican/refs/heads/main/assets/docs/site-is-live.png)

If you follow the link, you should be able to see your newly deployed website.

![View website](https://raw.githubusercontent.com/turbopelican/turbopelican/refs/heads/main/assets/docs/main-page.png)

You can learn more about Pelican [here](https://getpelican.com).

### Configuration

Pelican still targets Python 3.9, which does not bundle built-in support for
reading TOML configuration. Projects using `turbopelican` require Python 3.11
or higher, and therefore adopt the newer convention of placing configuration
in a TOML file rather than Python scripts. Generally, you should only need to
modify `turbopelican.toml`, rather than `pelicanconf.py` or `publishconf.py`.
