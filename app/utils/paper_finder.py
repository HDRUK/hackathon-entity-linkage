from utils.epmc import get_full_text_from_doi


class PaperFinder:
    def __init__(self, doi):
        self.soup = get_full_text_from_doi(doi)
        if not self.soup:
            raise ValueError(f"Could not fetch paper data for DOI: {doi}")

        self.title = self._get_title()
        self.abstract = self._get_abstract()
        self.results = self.find_section("results")
        self.introduction = self.find_section("introduction")
        self.methods = self.find_section("methods")
        self.code = self.find_notes("code availability")

    def _get_title(self):
        title_tag = self.soup.find("article-title")
        if title_tag:
            return title_tag.get_text(strip=True)
        raise ValueError("No title found in the paper.")

    def _get_abstract(self):
        abstract = self.soup.find("abstract")
        if abstract:
            return abstract.get_text(strip=True)
        raise ValueError("No abstract found in the paper.")

    def find_notes(self, name):
        for notes in self.soup.find_all("notes"):
            title = notes.find("title")
            if title and name.lower() in title.text.lower():
                return notes.get_text(separator=" ", strip=True)
        return None

    def find_section(self, name):
        for sec in self.soup.find_all("sec"):
            title = sec.find("title")
            if title and name.lower() in title.text.lower():
                return sec.get_text(separator=" ", strip=True)
        return None

    def get_paper_data(self):
        return {
            "title": self.title,
            "abstract": self.abstract,
            "results": self.results,
            "introduction": self.introduction,
            "methods": self.methods,
            "code": self.code,
        }
