Title: Prerequisites
Date: 2025-06-16

# Prerequisites

Before you run Turbopelican, there is a small handful of tasks you will need
to check off.

## Install uv

[uv](https://docs.astral.sh/uv/) is a *must-have* for any Python developer. In
brief, it lets you handle Python environments and packages with minimal fuss.
If you can install it successfully, you don't need to know anything more about
it to use Turbopelican.

## Install git

It should almost go without saying, but all developers should have
[git](https://git-scm.com) installed. This will allow you to source control
your website. It does help to have a basic understanding of git. Make sure
to configure your user name and email:

    :::sh
    git config --global user.name "John Doe"            # Insert your username here
    git config --global user.email "john.doe@gmail.com" # Insert your email address here


## Create a GitHub account

If you want to create a website via GitHub Pages, you will need to
get a [GitHub](https://github.com/) account. This provides you a simple way to
share your code (and your website) with the world.

You should also set up
[SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh)
if you haven't already. This will help GitHub to identify you when you try
modifying your website.

## Install GitHub CLI (optional)

It is not necessary but recommended to install
[GitHub CLI](https://docs.github.com/en/github-cli/github-cli/about-github-cli)
to run Turbopelican, but it will make things easier for you if you do. GitHub
CLI is a command-line tool which helps Turbopelican interact with GitHub.

Once you are all finished, you can at last [run Turbopelican](/get-started).
