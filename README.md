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
