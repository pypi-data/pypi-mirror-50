from smart_open import open
from os import path
import csv
from pathlib import Path
from xml.sax.saxutils import escape

ALLOWED_LETTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"


def check_letters(text):
    return min({l in ALLOWED_LETTERS for l in text}) if text else True

def toutf8mb3(t):
    return "".join([c if ord(c)<2**16 else "_e" for c in t])


class Corpus:
    def writeline(self, line):
        assert "\n" not in line
        self._fo.write(line + "\n")

    def writemeta(self, metadata):
        self._meta.writerow(metadata)

    def __init__(self, target_folder, name, pattrs, *args):
        target_folder = path.expanduser(target_folder)
        target_folder = Path(target_folder)
        assert path.isdir(target_folder)
        try:
            assert check_letters(name)
        except Exception as e:
            print("Wrong param is:'{}".format(name))
            raise e

        assert isinstance(pattrs, int)
        assert pattrs > 0
        self._pattrs = pattrs

        self.fieldnames = ["id"]
        for arg in args:
            assert check_letters(arg)
            self.fieldnames.append(arg)

        self._fo = open(
            path.join(target_folder, name + ".vrt.gz"),
            "w",
            encoding="utf8"
        )

        self._metaf = open(
            path.join(target_folder, name + ".meta.tsv"),
            "w",
            encoding="utf8",
            newline=""
        )

        self._meta = csv.DictWriter(self._metaf,
                                    fieldnames=self.fieldnames,
                                    delimiter="\t",
                                    lineterminator="\n"
                                    )

        self.writeline("<corpus>")

        self._idcount = -1

    def close(self):
        self.writeline("</corpus>")
        self._fo.close()
        self._metaf.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def getid(self):
        self._idcount += 1
        return "t{}".format(self._idcount)

    def add_spacy(self, spacymodel="de_core_news_sm", add_patrs=["tag_", "pos_", "lemma_"]):
        assert self._pattrs == 1 + len(add_patrs)

        try:
            import spacy
            self._nlp = spacy.load(spacymodel)
        except Exception as e:
            print("Spacy must be installed and model downloaded")
            print("For example you may execute 'python3 -m spacy download de_core_news_sm'")
            raise e

        allowed = ["ent_type_", "lower_", "norm_", "prefix_", "suffix_", "lemma_", "pos_", "tag_", "dep_"]
        for attr in add_patrs:
            assert attr in allowed
        self._add_patrs = add_patrs


class Sattribute:
    ATTRNAME = None

    def __init__(self, corpus, attrib_name):
        assert isinstance(corpus, Corpus)
        assert not corpus._fo.closed
        self.writeline = corpus.writeline
        self._pattrs = corpus._pattrs

    def writep(self, *args):
        assert len(args) == self._pattrs
        args = [toutf8mb3(escape(line)) for line in args]
        self.writeline("\t".join(args))

    def close(self):
        self.writeline("</{}>".format(self.ATTRNAME))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


class Text(Sattribute):
    ATTRNAME = "text"

    def __init__(self, corpus, **kwargs):
        super().__init__(corpus, self.ATTRNAME)
        assert "id" not in kwargs

        ident = corpus.getid()
        for argn, arg in kwargs.items():
            assert argn in corpus.fieldnames
            try:
                assert check_letters(arg)
            except Exception as e:
                print("Exception was thrown when checking '{}".format(arg))
                raise e
        self.writeline('<text id="{}">'.format(ident))
        kwargs["id"] = ident
        corpus.writemeta(kwargs)


class P(Sattribute):
    """
    This Class has no Metadata
    """
    ATTRNAME = "p"

    def __init__(self, corpus):
        super().__init__(corpus, self.ATTRNAME)
        self.writeline('<{}>'.format(self.ATTRNAME))


class S(Sattribute):
    """
    This Class has no Metadata
    """
    ATTRNAME = "s"

    def __init__(self, corpus):
        super().__init__(corpus, self.ATTRNAME)
        self.writeline('<{}>'.format(self.ATTRNAME))


def annotext_german(corpus, text, **kwargs):
    """
    Uses germalemma,
    :param corpus: reference to corpus class
    :param text: content of text
    :param kwargs: text-metadata conform with corpus settings
    :return:
    """
    assert isinstance(corpus, Corpus)
    assert corpus._pattrs == 4
    assert isinstance(text, str)
    with Text(corpus, **kwargs) as t:
        pass
        # TODO Great stuff


def annotext_spacy(corpus, text, **kwargs):
    """
    Uses spacy for creating annotext
    :param corpus: corpus object with loaded spacy
    :param text: string of corpus text
    :param kwargs: parameters for text metadata
    """

    assert isinstance(corpus, Corpus)
    try:
        nlp = corpus._nlp
        add_patrs = corpus._add_patrs
    except:
        raise Exception("Spacy not configured yet")

    assert corpus._pattrs == 1 + len(add_patrs)
    assert isinstance(text, str)

    with Text(corpus, **kwargs) as t:
        text = nlp(text.replace("\n", " "))
        for s in text.sents:
            with S(corpus) as sw:
                for w in s:
                    sw.writep(w.text, *[getattr(w, attr) for attr in add_patrs])

"""
def _testcode():
    with Corpus("~", "mycorpus", 4, "textname", "author") as c:
        c.add_spacy()
        text = "Das hier ist ein kurzer Test um das Modell auszuprobieren. Manchmal geht das, manchmal auch nicht ;)"
        annotext_spacy(c, text, textname="Demotext1", author="someZeit_guy")

        with Text(c, textname="Demotext2", author="Frank_N") as text:
            with P(c) as paragraph:
                with S(c) as s:
                    s.writep("Das", "PDS", "PRON", "der")
                    s.writep("hier","ADV","ADV","hier")
"""
