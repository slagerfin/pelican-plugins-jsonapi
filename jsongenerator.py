import os
import json
from pelican import signals
from pelican.generators import Generator


class JSONGenerator(Generator):
    def generate_context(self):
        pages = []
        articles = []
        print(dir(self.context.get('PAGES')[0]))
        for p in self.context.get('PAGES', []):
            if p.status != 'published':
                continue
            metadata = p.metadata.copy()
            metadata['category'] = p.metadata.get('category').name
            date = metadata.get('date')
            if date:
                metadata['date'] = str(date)
            pages.append({
                'title': p.title,
                'content': p.content,
                'translations': p.translations,
                'author': p.author.name,
                'url': p.url,
                'slug': p.slug,
                'summary': p.summary,
                'metadata': metadata,
                #'relative_dir': p.relative_dir
            })

        for a in self.context.get('ARTICLES', []):
            metadata = a.metadata.copy()
            metadata['category'] = p.metadata.get('category')
            articles.append({
                'title': a.title,
                'content': a.content,
                'translations': p.translations,
                'author': p.author.name,
                'date': str(a.date),
                'summary': a.summary,
                'url': a.url,
                'slug': a.slug,
                'metadata': metadata
            })

        self.context['jsonapi'] = {
            'articles': articles,
            'pages': pages,
            'page_index': list(map(self._get_page_metadata, pages)),
            'article_index': list(map(self._get_article_metadata, articles))
        }

    def generate_output(self, writer):
        base_path = os.path.join(writer.output_path, 'jsonapi')
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        index_data = {
            'pages': self.context['jsonapi']['page_index'],
            'articles': self.context['jsonapi']['page_index']
        }
        index_path = os.path.join(base_path, 'index.json')
        with open(index_path, 'w') as f:
            f.write(self._get_json(index_data))

        pages_path = os.path.join(base_path, 'pages')
        if not os.path.exists(pages_path):
            os.makedirs(pages_path)
        for p in self.context['jsonapi']['pages']:
            page_path = os.path.join(pages_path, p.get('slug'))
            with open(page_path, 'w') as f:
                f.write(self._get_json(p))

        articles_path = os.path.join(base_path, 'articles')
        if not os.path.exists(articles_path):
            os.makedirs(articles_path)
        for a in self.context['jsonapi']['articles']:
            page_path = os.path.join(articles_path, a.get('slug'))
            with open(page_path, 'w') as f:
                f.write(self._get_json(a))

    def _get_json(self, obj):
        return json.dumps(obj, indent=2)

    def _get_page_metadata(self, page):
        page = page.copy()
        for d in ['metadata', 'content', 'translations']:
            del page[d]
        return page

    def _get_article_metadata(self, article):
        article = article.copy()
        for d in ['metadata', 'content', 'translations']:
            del article[d]
        return article


def get_generators(pelican_object):
    return JSONGenerator

def register():
    signals.get_generators.connect(get_generators)
