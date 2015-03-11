**Heads up!** This software is in alpha.

# pelican-plugins-jsonapi
jsonapi is a pelican generator which exports pelican's pages and articles to a static JSON "API". It aims to help you to implement client side functionality to your pelican site more easily.

# Usage
Structure of the API in output directory is currently following:
- output/jsonapi/
  - index.json
  - pages/
    - page-title.json // files are named after slug attribute
    - another-page-title.json
  - articles/
    - article-title.json
    - another-article-title.json

Currently index.json file contains basic data of pages and articles:
<pre>
{
  "articles": [
    {
      "title": "Foo",
      "url": "articles/foo.json",
      "date": "2015-02-11 09:20:00+01:00",
      "author": "Samuli Lager",
      "summary": "<p>My first article!</p>"
    },
  ],
  "pages": [
    {
      "title": "Bar",
      "url": "pages/about-me.json",
      "author": "Samuli Lager",
      "summary": "<p>My first page!</p>"
    },
  ]
}
</pre>
