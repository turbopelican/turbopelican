# My turbopelican site

[![turbopelican](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/turbopelican/turbopelican/refs/heads/main/assets/badge/v2.json)](https://github.com/turbopelican/turbopelican)

Thank you for choosing
[turbopelican](https://github.com/turbopelican/turbopelican)!

## Development

You can add content to your website by modifying the `README.md` files in the
`contents` folder. In order to view your changes live, you can run the
following command:

```sh
cd project-folder
.venv/bin/pelican -r -l
```

You can then click on the hyperlink provided to view your website, hosted
locally.

In order to deploy your page, you will need to push the changes to your GitHub
repository.

### Theme

The theme provided in the `themes` folder is bare-bones, consisting of static
files and templates. In order to change the HTML of your different pages, you
should modify `themes/plain-theme/templates/page.html`.

If you want your website to be more flexible, do not forget that you can simply
embed HTML inside your Markdown files. For example:

```markdown
# My page
<p>I can write a paragraph, or really anything I like!</p>
This is just plain text.
```

Thus it is not necessary to modify a theme for minor differences in styling of
a page.

### Configuration

The `turbopelican.toml` file should contain all the configuration for pelican.
Not all settings Pelican offers are present, so either place it explicitly in
`pelicanconf.py` or `publishconf.py`, or open a pull request to map it across
from `turbopelican.toml`.

At present, the website is configured to serve for a generic website, rather
than a blog. Read more from the
[Pelican docs](https://docs.getpelican.com/en/latest/).
