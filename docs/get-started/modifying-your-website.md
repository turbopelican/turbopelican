Title: Modifying your website
Date: 2025-06-16

# Modifying your website

If you are not familiar with Pelican, it's easy to learn the basics quickly
with the default set up. Your new project should look something like this:

    mywebsite
    ├── pelicanconf.py
    ├── pyproject.toml
    ├── README.md
    ├── turbopelican.toml
    ├── uv.lock
    ├── content
    │   ├── images
    │   │   └── logo.svg
    │   ├── index.md
    │   ├── my-article.md
    │   └── static
    │       └── favicon.ico
    └── themes
        └── plain-theme
            ├── static
            │   └── css
            │       └── styles.css
            └── templates
                ├── archives.html
                ├── aritcle.html
                ├── author.html
                ├── base.html
                ├── categories.html
                ├── category.html
                ├── index.html
                ├── page.html
                ├── period_archives.html
                ├── tag.html
                └── tags.html

The `themes` directory is where you place the wrapper HTML that is copied from
page to page. Though there are many different templates on display, the theme
provided only uses `base.html`, while the other `*.html` templates are empty.
For now, modify `base.html` if you want all your pages to look different.

You will notice a single CSS file `themes/plain-theme/static/css/styles.css`.
Edit this file to change your website's styling.

The general rule is that your website's content (i.e. articles, blog posts,
documentation, etc.) is stored within `content`, along with any media you want
in your website, such as images. To create new content, create a
[Markdown](https://www.markdownguide.org/basic-syntax/) file in which you can
write like so:

    :::markdown
    ### Hello

    This is a paragraph.

    1. This
    2. Is
    3. A
    4. List

    <p>I can also write HTML here!</p>

Turbopelican comes with a flat page structure out of the box, so if you create
`content/my-article.md` for a website at `https://mywebsite.github.io`, you
can access it at `https://mywebsite.github.io/my-article`. The exception is
`content/index.md`, which is rendered at `https://mywebsite.github.io`.

## Previewing your modifications

If you wish to preview your website *before* you push changes to GitHub (which
is generally sensible), you navigate to your directory and run the following
command:

    :::sh
    $ uv run pelican -r -l
     --- AutoReload Mode: Monitoring `content`, `theme` and `settings` for changes. ---
    Serving site at: http://127.0.0.1:8000 - Tap CTRL-C to stop
    Done: Processed 0 articles, 0 drafts, 0 hidden articles, 2 pages, 0 hidden pages and 0 draft pages in 0.11 seconds.

This will serve your website from localhost. Follow the hyperlink and you will
be able to make sure that your website is what you expect.

Of course, the default theme is rather plain. To give your website a fresh
splash of paint, you will need to modify your theme. If you are finding that
Turbopelican's default configuration is too restrictive for your purposes, you
will need to [configure Turbopelican](/configuration).
