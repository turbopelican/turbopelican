Title: Get started
Date: 2025-06-16

# Get started

Before you try Turbopelican, make sure that all
[prerequisites](/get-started/prerequisites) are met.

## Run Turbopelican

If you have chosen to install
[GitHub CLI](https://docs.github.com/en/github-cli/github-cli/about-github-cli)
already, then you can run the following command:

    :::sh
    uvx turbopelican init mywebsite --use-gh-cli

Otherwise you can run:

    :::sh
    uvx turbopelican init mywebsite

where `mywebsite` is the name of the repository you wish to create. In either
case, you will be prompted for a number of settings.

    :::sh
    $ uvx turbopelican init mywebsite --use-gh-cli
    Who is the website author? [John Doe] 
    What is the name of the website? [mywebsite]
    What timezone will your website use? [Australia/Sydney] 
    What language will your website use? [en]
    What is your website URL? [https://mywebsite.github.io]

Of course, the defaults will depend on your system. In general, you can choose
a website author and website name arbitrarily. If the default timezone is not
correct, and you are not sure what timezone to use, you can check on
[Wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)
in the column "**TZ identifier**" for a list of acceptable timezones. Likewise
for the language, if the default is incorrect and you are not sure what
language code, check on
[Wikipedia](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes#Table)
for a list of ISO 639 compliant language codes.

The most important setting is the website URL, and this will depend on your
GitHub user/organization name. If your GitHub account is called `john-doe`,
then you should input `https://john-doe.github.io` as your URL.

Once you have provided answers to the questions, Turbopelican will create a
new repository for you. If you installed GitHub CLI and used the
`--use-gh-cli` flag, your new repository will be automatically pushed to
GitHub, and you can skip the next section. If you did not use the
`--use-gh-cli` flag, read on.

## Push code to GitHub

Once you have created your new repository, you need to push your code to
GitHub. First, you will need to log into GitHub and
[create a new repository](https://github.com/new). Be sure that the repository
is equal to the owner's name (your username or organization name) with the
suffix `.github.io` at the end. I.e. if you are creating a repository to be
owned by user `john-doe`, you should name the repository `john-doe.github.io`.

<figure>
    <img src="/images/create-repo.png" />
</figure>

Make sure that the repository is public (otherwise GitHub Actions will not
deploy your website). Do not add a `README` file or any other files. The
repository shouldn't contain anything on creation.

After the repository has been created, copy the git repository URL. You will
need it later.

<figure>
    <img src="/images/get-repo-reference.png" />
</figure>

Then enter your settings for your repository and under "**Code and
automation**" click "**Pages**". The section "**Build and deployment**" allows
you to choose a source. Choose "**GitHub actions**".

<figure>
    <img src="/images/github-actions-settings.png" />
</figure>

Now you are ready to push your code to Github:

    :::sh
    cd mywebsite
    git remote add origin git@github.com:mywebsite/mywebsite.github.io.git # Use your own git repo reference
    git push --set-upstream origin main

## View your website

Now navigate to the webpage for your repository, and you should see it now has
contents:

<figure>
    <img src="/images/view-new-repo.png" />
</figure>

Now navigate back to the settings where you configure GitHub Pages, and you
should be able to see (it may take a short period of time) that your website
has been deployed.

<figure>
    <img src="/images/site-is-live.png" />
</figure>

Follow the link (this URL be the same as your site URL you defined earlier)
and you should see your new website:

<figure>
    <img src="/images/main-page.png" />
</figure>

Whenever you push changes from your local Git repository to GitHub, this
website will update. Learn more about how to modify your website
[here](/get-started/modifying-your-website).
