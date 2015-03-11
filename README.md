**Heads up!** This software is in alpha.

# pelican-plugins-jsonapi
jsonapi is a pelican generator which exports pelican's pages and articles to a static JSON "API". It aims to help you to implement client side functionality to your pelican site more easily.

# Usage
Structure of the API in output directory is currently following:
- output/jsonapi/
  - index.json
  - articles/
    - foo.json
  - pages/
    - bar.json


Currently index.json file contains basic data of pages and articles:
<pre><code>
{
  "articles": [
    {
      "title": "Foo",
      "url": "articles/foo.json",
      "date": "2015-02-11 09:20:00+01:00",
      "author": "Samuli Lager",
      "summary": "My first  article!",
    },
  ],
  "pages": [
    {
      "title": "Bar",
      "url": "pages/bar.json",
      "author": "Samuli Lager",
      "summary": "My first page!",
    },
  ]
}
</code></pre>
