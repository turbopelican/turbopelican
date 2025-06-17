Title: Configuration
Date: 2025-06-16

# Configuration

Turbopelican eliminates the need to use two scripts (`pelicanconf.py` and
`publishconf.py`) for configuring Pelican by providing a `pelicanconf.py`
script which will correctly load the appropriate configuration depending on
your situation. As a result, you will want to modify your `turbopelican.toml`
configuration file. You **do not** need to modify `pelicanconf.py`.

## Using TOML to configure Pelican

Pelican has a
[number of settings](https://docs.getpelican.com/en/latest/settings.html#basic-settings)
which can be changed according to your need. Turbopelican allows you to define
them in `turbopelican.toml` instead. By default it should look something like
this:

    :::toml
    [pelican]
    author = "Elliot Simpson"
    sitename = "MySite"

    timezone  = "Pacific/Auckland"

    default_lang = "en"

    path = "content"

    default_pagination = false

    theme = "themes/plain-theme"

    article_paths = []
    page_paths = [""]
    page_save_as = "{slug}.html"

    static_paths = ["static", "images"]

    index_save_as = ""

    author_feed_atom = "None"
    author_feed_rss = "None"
    category_feed_atom = "None"
    feed_all_atom = "None"
    translation_feed_atom = "None"

    [[pelican.extra_path_metadata]]
    origin = "static/favicon.ico"
    path = "favicon.ico"

    [[pelican.extra_path_metadata]]
    origin = "images/logo.svg"
    path = "logo.svg"

    [publish]
    site_url = "https://turbopelican.github.io"
    relative_urls = false
    feed_all_atom = "feeds/all.atom.xml"
    category_feed_atom = "feeds/{slug}.atom.xml"
    delete_output_directory = true

The simple rule is that settings under `[pelican]` configure Pelican during
development, while settings under `[publish]` configure Pelican during
publication. Because most of your settings will be mostly the same in both
contexts, settings not defined in `[publish]` will fallback to those defined
in `[pelican]` if possible.

The name of all settings should be the same as those in `Pelican`, except
lowercase. The only exception is `SITEURL` which is written within the TOML as
`site_url` with an underscore.

Where Pelican expects tuples or lists, use arrays. Where Pelican expects
dictionaries, use tables. There is one exception to this. The
`EXTRA_PATH_METADATA` setting in Pelican needs to be a dictionary, for
example:

    :::python
    EXTRA_PATH_METADATA = {
        "static/favicon.ico": {"path": "favicon.ico"},
        "images/logo.svg": {"path": "logo.svg"},
    }

To achieve this in `turbopelican.toml`, the keys of `EXTRA_PATH_METADATA` are
flattened into the values with the key `"origin"`:

    :::toml
    [[pelican.extra_path_metadata]]
    origin = "static/favicon.ico"
    path = "favicon.ico"

    [[pelican.extra_path_metadata]]
    origin = "images/logo.svg"
    path = "logo.svg"

Refer to the Pelican documentation for what each setting does.

### Special values

The `pelicanconf.py` file needs to be capable of containing settings with
values of `None`. In some cases, certain settings will need to contain
functions. TOML does not natively contain either of these concepts.

#### None values

By default, Turbopelican will swap any `"None"` string values for `None`. If
this causes an issue, it is possible to change the sentinel value
(`meta.null_sentinel`) to something like `-1`:

    :::toml
    [meta]
    null_sentinel = -1

    [pelican]
    analytics = -1 # Becomes `None`

Or `"TurboPelicanNull"` like so:

    :::toml
    [meta]
    null_sentinel = "TurboPelicanNull"

    [pelican]
    author = "TurboPelicanNull" # Becomes `None`

#### Functions

Breaking the strictest conventions of configuration, Pelican can be configured
with functions. Though TOML has no native concept of functions, Turbopelican
lets you parse strings as functions like so:

    :::toml
    [[meta.module_prefix]]
    prefix = "@urlencode:"
    module_name = "custom_filter"

    [pelican]
    jinja_filters = {urlencode = "@urlencode:urlencode_filter"}

This is equivalent to the following Python:

    :::python
    from custom_filter import urlencode_filter


    JINJA_FILTERS = {
        "urlencode": urlencode_filter
    }

Whenever a `prefix` value is found beneath `[pelican]` or `[publish]`, the
subsequent string is treated as the name of the function to be imported from
the module with the specified `module_name`. Note that this means the module
should be found from the `PYTHONPATH`.

<details>
    <summary>Configuration settings index</summary>
    <ul style="column-count: 2;">
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#ANALYTICS">analytics</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#ARCHIVES_SAVE_AS">archives_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#ARTICLE_EXCLUDES">article_excludes</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#ARTICLE_LANG_SAVE_AS">article_lang_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#ARTICLE_LANG_URL">article_lang_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#ARTICLE_ORDER_BY">article_order_by</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#ARTICLE_PATHS">article_paths</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#ARTICLE_SAVE_AS">article_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#ARTICLE_TRANSLATION_ID">article_translation_id</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#ARTICLE_URL">article_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#AUTHOR">author</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#AUTHORS_SAVE_AS">authors_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#AUTHOR_FEED_ATOM">author_feed_atom</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#AUTHOR_FEED_ATOM_URL">author_feed_atom_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#AUTHOR_FEED_RSS">author_feed_rss</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#AUTHOR_FEED_RSS_URL">author_feed_rss_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#AUTHOR_REGEX_SUBSTITUTIONS">author_regex_substitutions</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#AUTHOR_SAVE_AS">author_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#AUTHOR_URL">author_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#BIND">bind</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CACHE_CONTENT">cache_content</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CACHE_PATH">cache_path</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CATEGORIES_SAVE_AS">categories_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CATEGORY_FEED_ATOM">category_feed_atom</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CATEGORY_FEED_ATOM_URL">category_feed_atom_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CATEGORY_FEED_RSS">category_feed_rss</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CATEGORY_FEED_RSS_URL">category_feed_rss_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CATEGORY_REGEX_SUBSTITUTIONS">category_regex_substitutions</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CATEGORY_SAVE_AS">category_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CATEGORY_URL">category_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CHECK_MODIFIED_METHOD">check_modified_method</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CONTENT_CACHING_LAYER">content_caching_layer</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#CSS_FILE">css_file</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DATE_FORMATS">date_formats</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DAY_ARCHIVE_SAVE_AS">day_archive_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DAY_ARCHIVE_URL">day_archive_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DEFAULT_CATEGORY">default_category</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DEFAULT_DATE_FORMAT">default_date_format</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DEFAULT_LANG">default_lang</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DEFAULT_METADATA">default_metadata</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DEFAULT_ORPHANS">default_orphans</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DEFAULT_PAGINATION">default_pagination</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DELETE_OUTPUT_DIRECTORY">delete_output_directory</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DIRECT_TEMPLATES">direct_templates</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DISPLAY_CATEGORIES_ON_MENU">display_categories_on_menu</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DISPLAY_PAGES_ON_MENU">display_pages_on_menu</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DISQUS_SITENAME">disqus_sitename</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DOCUTILS_SETTINGS">docutils_settings</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DRAFT_LANG_SAVE_AS">draft_lang_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DRAFT_LANG_URL">draft_lang_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DRAFT_PAGE_LANG_SAVE_AS">draft_page_lang_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DRAFT_PAGE_LANG_URL">draft_page_lang_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DRAFT_PAGE_SAVE_AS">draft_page_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DRAFT_PAGE_URL">draft_page_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DRAFT_SAVE_AS">draft_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#DRAFT_URL">draft_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#EXTRA_PATH_METADATA">extra_path_metadata</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FEED_ALL_ATOM">feed_all_atom</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FEED_ALL_ATOM_URL">feed_all_atom_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FEED_ALL_RSS">feed_all_rss</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FEED_ALL_RSS_URL">feed_all_rss_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FEED_APPEND_REF">feed_append_ref</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FEED_ATOM">feed_atom</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FEED_ATOM_URL">feed_atom_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FEED_DOMAIN">feed_domain</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FEED_MAX_ITEMS">feed_max_items</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FEED_RSS">feed_rss</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FEED_RSS_URL">feed_rss_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FILENAME_METADATA">filename_metadata</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#FORMATTED_FIELDS">formatted_fields</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#GITHUB_URL">github_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#GZIP_CACHE">gzip_cache</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#IGNORE_FILES">ignore_files</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#INDEX_SAVE_AS">index_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#INTRASITE_LINK_REGEX">intrasite_link_regex</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#JINJA_ENVIRONMENT">jinja_environment</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#JINJA_FILTERS">jinja_filters</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#JINJA_GLOBALS">jinja_globals</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#JINJA_TESTS">jinja_tests</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#LINKS">links</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#LINKS_WIDGET_NAME">links_widget_name</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#LOAD_CONTENT_CACHE">load_content_cache</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#LOCALE">locale</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#LOG_FILTER">log_filter</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#MARKDOWN">markdown</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#MENUITEMS">menuitems</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#MONTH_ARCHIVE_SAVE_AS">month_archive_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#MONTH_ARCHIVE_URL">month_archive_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#NEWEST_FIRST_ARCHIVES">newest_first_archives</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#OUTPUT_PATH">output_path</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#OUTPUT_RETENTION">output_retention</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#OUTPUT_SOURCES">output_sources</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#OUTPUT_SOURCES_EXTENSION">output_sources_extension</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PAGE_EXCLUDES">page_excludes</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PAGE_LANG_SAVE_AS">page_lang_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PAGE_LANG_URL">page_lang_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PAGE_ORDER_BY">page_order_by</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PAGE_PATHS">page_paths</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PAGE_SAVE_AS">page_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PAGE_TRANSLATION_ID">page_translation_id</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PAGE_URL">page_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PAGINATED_TEMPLATES">paginated_templates</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PAGINATION_PATTERNS">pagination_patterns</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PATH">path</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PATH_METADATA">path_metadata</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PLUGINS">plugins</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PLUGIN_PATHS">plugin_paths</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PORT">port</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#PYGMENTS_RST_OPTIONS">pygments_rst_options</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#READERS">readers</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#RELATIVE_URLS">relative_urls</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#REVERSE_CATEGORY_ORDER">reverse_category_order</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#RSS_FEED_SUMMARY_ONLY">rss_feed_summary_only</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SITENAME">sitename</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SITESUBTITLE">sitesubtitle</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SITEURL">site_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SLUGIFY_PRESERVE_CASE">slugify_preserve_case</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SLUGIFY_SOURCE">slugify_source</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SLUGIFY_USE_UNICODE">slugify_use_unicode</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SLUG_REGEX_SUBSTITUTIONS">slug_regex_substitutions</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SOCIAL">social</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SOCIAL_WIDGET_NAME">social_widget_name</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#STATIC_CHECK_IF_MODIFIED">static_check_if_modified</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#STATIC_CREATE_LINKS">static_create_links</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#STATIC_EXCLUDES">static_excludes</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#STATIC_EXCLUDE_SOURCES">static_exclude_sources</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#STATIC_PATHS">static_paths</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#STYLESHEET_URL">stylesheet_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SUMMARY_END_SUFFIX">summary_end_suffix</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SUMMARY_MAX_LENGTH">summary_max_length</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#SUMMARY_MAX_PARAGRAPHS">summary_max_paragraphs</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TAGS_SAVE_AS">tags_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TAG_FEED_ATOM">tag_feed_atom</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TAG_FEED_ATOM_URL">tag_feed_atom_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TAG_FEED_RSS">tag_feed_rss</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TAG_REGEX_SUBSTITUTIONS">tag_regex_substitutions</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TAG_SAVE_AS">tag_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TAG_URL">tag_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TEMPLATE_EXTENSIONS">template_extensions</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TEMPLATE_PAGES">template_pages</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#THEME">theme</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#THEME_STATIC_DIR">theme_static_dir</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#THEME_STATIC_PATHS">theme_static_paths</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#THEME_TEMPLATES_OVERRIDES">theme_templates_overrides</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TIMEZONE">timezone</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TRANSLATION_FEED_ATOM">translation_feed_atom</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TRANSLATION_FEED_ATOM_URL">translation_feed_atom_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TRANSLATION_FEED_RSS">translation_feed_rss</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TRANSLATION_FEED_RSS_URL">translation_feed_rss_url</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TWITTER_USERNAME">twitter_username</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TYPOGRIFY">typogrify</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TYPOGRIFY_DASHES">typogrify_dashes</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TYPOGRIFY_IGNORE_TAGS">typogrify_ignore_tags</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#TYPOGRIFY_OMIT_FILTERS">typogrify_omit_filters</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#USE_FOLDER_AS_CATEGORY">use_folder_as_category</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#WITH_FUTURE_DATES">with_future_dates</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#YEAR_ARCHIVE_SAVE_AS">year_archive_save_as</a>
        </li>
        <li>
            <a href="https://docs.getpelican.com/en/latest/settings.html#YEAR_ARCHIVE_URL">year_archive_url</a>
        </li>
    </ul>
</details>
