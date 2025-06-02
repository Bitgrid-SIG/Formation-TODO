
from bs4.element import PageElement, Tag, NavigableString
from bs4 import BeautifulSoup
import requests

from typing import (
    TypeAlias, Generic, TypeVar,
    List, Dict,

    cast,
)

from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum
import os


T = TypeVar('T')
class NonEmptyList(List[T], Generic[T]):
    def __init__(self, items: List[T]) -> None:
        if not items:
            raise ValueError("NonEmptyList must contain at least one item")
        super().__init__(items)


@dataclass
class Link:
    contents:   str
    href:       str

    @classmethod
    def from_tag(cls, tag: Tag) -> 'Link':
        assert tag.name == 'a', 'Only anchor tags can be made into a Link!'
        href: str = cast(str, tag.attrs['href']) if tag.attrs['href'] is str else tag.attrs['href'][0]
        return Link(contents=tag.text, href=href)
    
    def __str__(self):
        return f'[[{self.contents}]({self.href})]'
    
    def __eq__(self, other: 'Link') -> bool:
        return self.contents == other.contents and self.href == other.href
    
    def __hash__(self) -> int:
        return hash((self.contents, self.href))


WorkingGroup: TypeAlias = Link
class WebStandardEntryType(StrEnum):
    NOTE = 'note'
    DRAFT_NOTE = 'draft note'
    DRAFT_STANDARD = 'draft standard'
    DRAFT_REGISTRY = 'draft registry'
    CANDIDATE_STANDARD = 'candidate standard'
    QUALIFIED_STANDARD = 'standard'
    STATEMENT = 'statement'


@dataclass
class WebStandard:
    section:        str
    title:          Link
    status:         WebStandardEntryType
    tags:           List[str]
    deliverers:     NonEmptyList[WorkingGroup]
    translations:   Link

    def __str__(self) -> str:
        status = '' if self.status == WebStandardEntryType.QUALIFIED_STANDARD else f'`{self.status}`'
        results = f'    - [ ] {self.title} {status}\n'
        
        results += '        - Deliverers: '
        results += ', '.join([str(d) for d in self.deliverers])
        results += '\n'

        if len(self.tags) > 0:
            results += '        - Tags: '
            results += ', '.join(self.tags)
            results += '\n'

        if len(self.translations) > 0:
            results += '        - Translations: '
            results += ', '.join([str(d) for d in self.translations])
            results += '\n'

        return results


def parse_web_standards(html: str) -> Dict[str, WebStandard]:
    soup = BeautifulSoup(html, 'html.parser')
    results: Dict[str, WebStandard] = defaultdict(list)

    for sec in soup.find_all('section', class_='family-grouping'):
        section_name = sec.find('h2').get_text(strip=True)

        for item in sec.find_all('div', class_='tr-list__item'):
            a = item.find('div', class_='tr-list__item__header').find('h3').find('a')
            title = Link(contents=a.get_text(strip=True), href=a['href'])
            status = item.find('span', class_='maturity-level').get_text(strip=True).lower()
            assert status in WebStandardEntryType._value2member_map_, f'{status} is not a valid status'

            tags: List[str] = []
            deliverers: List[WorkingGroup] = []
            translations: List[Link] = []

            dl = item.find('dl', class_='inline')
            for meta in dl.find_all('div'):
                meta_key = meta.find('dt').get_text(strip=True).split(' ')[0].lower()
                if meta_key == 'tags':
                    for meta_data in meta.find_all('dd'):
                        tags.append(meta_data.text.strip())

                elif meta_key == 'deliverers':
                    for meta_data in meta.find_all('dd'):
                        a = meta_data.find('a')
                        deliverers.append(Link(a.text.strip(), a.attrs['href']))

                elif meta_key in ['translation', 'translations', 'translationfor', 'translationsfor']:
                    for meta_data in meta.find_all('dd'):
                        a = meta_data.find('a')
                        translations.append(Link(a.text.strip(), a.attrs['href']))

            ws = WebStandard(
                section=section_name,
                title=title,
                status=status,
                tags=tags,
                deliverers=deliverers,
                translations=translations
            )
            results[ws.section].append(ws)

    return results

def get_page() -> str:
    if not os.path.exists('./standards.html'):
        standards_url: str = 'https://www.w3.org/TR/'
        response = requests.get(url=standards_url)
        response.raise_for_status()

        with open('./standards.html', 'wb') as file:
            file.write(response.text.encode())

        return response.text
    
    else:
        with open('./standards.html', 'rb') as file:
            return file.read().decode()

def main():
    source = get_page()
    standards = parse_web_standards(source)

    results = ''
    keys = list(standards.keys())
    keys.sort()
    for section in keys:
        results += f'- {section}\n'

        def filter_by_type(type: WebStandardEntryType):
            return list(filter(lambda s: s.status == type, standards[section]))
        
        standards[section].sort(key=lambda e: e.title.contents)

        statements = filter_by_type(WebStandardEntryType.STATEMENT)
        if len(statements) > 0:
            for standard in statements:
                results += str(standard)

        qualified = filter_by_type(WebStandardEntryType.QUALIFIED_STANDARD)
        if len(qualified) > 0:
            for standard in qualified:
                results += str(standard)
            continue
        
        candidates = filter_by_type(WebStandardEntryType.CANDIDATE_STANDARD)
        if len(candidates) > 0:
            for standard in candidates:
                results += str(standard)
            continue
        
        drafts = filter_by_type(WebStandardEntryType.DRAFT_STANDARD)
        if len(drafts) > 0:
            for standard in drafts:
                results += str(standard)
            continue
        
        notes = filter_by_type(WebStandardEntryType.NOTE)
        if len(notes) > 0:
            for standard in notes:
                results += str(standard)
            continue
        
        if len(statements) == 0:
            print(f'No entries to print in section {section}')

    with open('../STANDARDS.md', 'wb') as file:
        file.write(results.encode())
    
    working_groups = []
    for s in standards.keys():
        for e in standards[s]:
            working_groups.extend(e.deliverers)
    working_groups = list(set(working_groups))
    working_groups.sort(key=lambda g: g.contents)
    with open('../WORKING-GROUPS.md', 'wb') as file:
        content = f'- ' + '\n- '.join([str(g) for g in working_groups])
        file.write(content.encode())

    print('Done.')


if __name__ == '__main__':
    main()
    # pass
