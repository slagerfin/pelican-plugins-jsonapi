import os
import json
from pelican import signals
from pelican.generators import Generator

JSON_INDENT = 2
DEFAULT_JSON_PATH = 'jsonapi'
EXTENSION = 'json'

class JSONGenerator(Generator):
    serialize_cases = {
        'Author':       '_get_serializable_author',
        'SafeDatetime': '_get_serializable_date',
        'Category':     '_get_serializable_category',
    }

    def _get_serializable_author(self, author):
        return author.name

    def _get_serializable_category(self, category):
        return category.name

    def _get_serializable_date(self, safe_date):
        return str(safe_date)

    def _get_serializable(self, obj):
        f_name = JSONGenerator.serialize_cases.get(obj.__class__.__name__)
        if not f_name:
            return obj
        return getattr(self, f_name)(obj)

    def _get_url(self, obj):
        return os.path.join(obj.relative_dir, '{0}.{1}'.format(obj.slug, EXTENSION))

    def _get_page_metadata(self, page):
        metadata = page.metadata.copy()
        metadata['category'] = self._get_serializable(page.metadata.get('category'))
        date = self._get_serializable(metadata.get('date'))
        if date:
            metadata['date'] = self._get_serializable(date)
        modified = self._get_serializable(metadata.get('modified'))
        if modified:
            metadata['modified'] = self._get_serializable(modified)
        metadata['authors'] = list(map(self._get_serializable, metadata['authors']))
        return metadata

    def _get_article_metadata(self, article):
        metadata = article.metadata.copy()
        metadata['category'] = self._get_serializable(article.metadata.get('category'))
        date = self._get_serializable(metadata.get('date'))
        if date:
            metadata['date'] = self._get_serializable(date)
        modified = self._get_serializable(metadata.get('modified'))
        if modified:
            metadata['modified'] = self._get_serializable(modified)
        metadata['authors'] = list(map(self._get_serializable_author, metadata['authors']))
        return metadata

    def _get_article_indexdata(self, article):
        article = article.copy()
        for d in ['metadata', 'content', 'translations', 'slug']:
            del article[d]
        return article

    def _get_page_indexdata(self, page):
        page = page.copy()
        for d in ['metadata', 'content', 'translations', 'slug']:
            del page[d]
        return page

    def _get_cleaned_page(self, page):
        pass

    def _get_cleaned_article(self, page):
        pass


    def generate_context(self):
        pages = []
        articles = []

        for p in self.context.get('PAGES', []):
            if p.status != 'published':
                continue
            pages.append({
                'title': p.title,
                'content': p.content,
                'translations': p.translations,
                'author': self._get_serializable(p.author),
                'url': self._get_url(p),
                'slug': p.slug,
                'summary': p.summary,
                'metadata': self._get_page_metadata(p),
            })
        for a in self.context.get('articles', []):
            articles.append({
                'title': a.title,
                'content': a.content,
                'translations': p.translations,
                'author': self._get_serializable(a.author),
                'date': self._get_serializable(a.date),
                'url': self._get_url(a),
                'slug': a.slug,
                'summary': p.summary,
                'metadata': self._get_article_metadata(a)
            })
        self.context['jsonapi'] = {
            'articles': articles,
            'pages': pages,
            'page_index': list(map(self._get_page_indexdata, pages)),
            'article_index': list(map(self._get_article_indexdata, articles))
        }

    def generate_output(self, writer):
        api_path = self.context.get('JSONAPI_PATH', DEFAULT_JSON_PATH)
        base_path = os.path.join(writer.output_path, api_path)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        indexdata = {
            'pages': self.context['jsonapi']['page_index'],
            'articles': self.context['jsonapi']['article_index']
        }
        self._write_indexdata(base_path, indexdata)
        self._write_pages(base_path, self.context['jsonapi']['pages'])
        self._write_articles(base_path, self.context['jsonapi']['articles'])


    def _write_indexdata(self, indexdata):
        index_path = os.path.join(base_path, 'index.{0}'.format(EXTENSION))
        with open(index_path, 'w') as f:
            f.write(self._get_json(index_data))

    def _write_pages(self, pages, base_path):
        pages_path = os.path.join(base_path, 'pages')
        if not os.path.exists(pages_path):
            os.makedirs(pages_path)
        for p in pages:
            page_path = os.path.join(pages_path, '{0}.{1}'.format(p.get('slug'), EXTENSION))
            with open(page_path, 'w') as f:
                f.write(self._get_json(p))

    def _write_articles(self, pages, base_path):
        articles_path = os.path.join(base_path, 'articles')
        if not os.path.exists(articles_path):
            os.makedirs(articles_path)
        for a in self.context['jsonapi']['articles']:
            article_path = os.path.join(articles_path, '{0}.{1}'.format(a.get('slug'), EXTENSION))
            with open(article_path, 'w') as f:
                f.write(self._get_json(a))

    def _get_json(self, obj):
        return json.dumps(obj, indent=JSON_INDENT)


def get_generators(pelican_object):
    return JSONGenerator

def register():
    signals.get_generators.connect(get_generators)
