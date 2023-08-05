from collections import defaultdict
import html
import io
import logging
from lxml import etree, objectify
import os.path
import re
import unicodedata

import xmltodict


log = logging.getLogger(__name__)


def flatten_dict(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        # new_key = parent_key + sep + k if parent_key else k
        new_key = k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class TEIDocument:
    """This class represents a TEI-document

    Parameters
    ----------
    parser:
        An instance of an etree.XMLParser.
    """

    def __init__(self, src=None, **kwargs):
        self.parser = etree.XMLParser(recover=True, **kwargs)
        self.tree = None
        self.nsmap = None
        if src:
            self.load(src)

    @classmethod
    def from_tree(cls, tree):
        td = cls()
        td.tree = tree
        td.nsmap = td._get_nsmap()
        return td

    def load(self, source):
        """ Read source from file and parse it.

        Parameters
        ----------
        source: string containing the path to an source-file or source.
        """
        if not source:
            raise ValueError("No file provided")

        # if isinstance(source, io.IOBase):
        if hasattr(source, "read"):
            xml = source.read()
        elif os.path.isfile(os.path.abspath(os.path.expanduser(source))):
            with open(os.path.expanduser(source), "r") as f:
                xml = f.read()
        else:
            xml = source
            # raise TypeError(f"Cannot load source of type {type(source)}")

        if isinstance(xml, bytes):
            xml = xml.decode()

        xml = html.unescape(xml).encode("utf-8")

        self.tree = etree.fromstring(xml, self.parser)

        if "TEI" not in self.docinfo("root_name"):
            raise TypeError("Not a TEI-document")

        self.nsmap = self._get_nsmap()
        log.debug(f"loaded: {type(self.tree)}")

    def docinfo(self, attr=None):
        di = self._as_ElementTree().docinfo
        info = {
            "doctype": di.doctype,
            "encoding": di.encoding,
            "externalDTD": di.externalDTD,
            "internalDTD": di.internalDTD,
            "public_id": di.public_id,
            "root_name": di.root_name,
            "standalone": di.standalone,
            "system_url": di.system_url,
            "xml_version": di.xml_version,
        }
        if attr:
            return info.get(attr, None)
        else:
            return info

    def metadata(self):
        """Return a dict with the teiHeader data."""

        teiHeader = self.tree.xpath("//tei:teiHeader//tei:fileDesc", namespaces=self.nsmap)[0]
        md = flatten_dict(xmltodict.parse(etree.tostring(teiHeader), xml_attribs=False))
        log.debug(f"metadata: {md}")
        return md

    def entities(self):
        """Return the attributes of all <rs>-tags in the document.

        Entities such as 'parents' are a nnotated as two entities, key='524 526',
        so they'll be represented as separate persons

        TODO: include names

        """
        entities = defaultdict(list)
        if self.nsmap:
            expr = "//tei:rs"
        else:
            expr = "//rs"

        for e in self.tree.xpath(expr, namespaces=self.nsmap):
            ents = entities[e.get("type")]
            entities[e.get("type")].extend(
                # filter
                [k for k in e.get("key", "").split() if k not in ents]
            )
        return entities

    def text(self, kind=None):
        """
        Extract text from the divs in the text-element

        Parameters:
        -----------
            kind: if None, return a defaultdict(list) of 'type': [text, ...] pairs. If specified, return a list
            containing the text found in divs of that kind

        Raises:
        -------
            AttributeError: if someone forgot to load the xml
            KeyError: if kind is specified but not present in the document


        """
        if self.tree is None:
            raise AttributeError(f"{self.__class__}: could not parse xml")

        text = defaultdict(list)
        expr = "//tei:text//tei:body//tei:div"
        if not self.nsmap:
            expr = expr.replace("tei:", "")

        log.debug(f"using namespaces: {self.nsmap}")

        for d in self.tree.xpath(expr, namespaces=self.nsmap):
            layer = []
            for element in d:
                if element.tag is etree.Comment:
                    log.debug(f"skipped comment {etree.tostring(element)}")
                    continue
                # prevent nested layers
                if self._clean_tag(element) == "div":
                    log.debug(f"nested div found in /{'/'.join(self._ancestors(element))}")
                    continue
                layer.append(element.xpath("string()").strip())
            text[d.get("type", "default")].append(" ".join(layer))
        log.debug(f"layers: {text.keys()}")

        if kind:
            if kind in text:
                return text[kind]
            else:
                raise KeyError(f"{kind} not in text")
        return text

    def _ancestors(self, element):
        return [self._clean_tag(e) for e in reversed(list(element.iterancestors()))]

    def _descendants(self, element):
        return [self._clean_tag(e) for e in reversed(list(element.iterdescendants()))]

    def _as_xpath(self, element):
        attr = ", ".join(f"@{k}=\"{v}\"" for k, v in element.items())
        return f"{element}[{attr}]" if attr else f"{element}"

    def _clean_tag(self, element):
        try:
            return etree.QName(element).localname
        except ValueError as err:
            log.debug(err, f"tag: {etree.tostring(element)}", f"{element.name}", sep="\n")
            return "COMMENT"

    def _as_ElementTree(self):
        return etree.ElementTree(self.tree)

    def _get_nsmap(self):
        """ Return a tree's namespaces, mapped to prefixes.

        the default namespace is replaced with 'tei'
        """
        nsmap = None
        if isinstance(self.tree, etree._ElementTree):
            nsmap = self.tree.getroot().nsmap
        elif isinstance(self.tree, etree._Element):
            nsmap = self.tree.nsmap

        if not nsmap:
            log.warning(f"No namespaces in document.")
        else:
            nsmap["tei"] = nsmap.pop(None)
            log.debug(f"Replaced default namespace: {nsmap}")
        return nsmap

    def _strip_namespaces(self):
        root = etree.fromstring(etree.tostring(self.tree))
        for element in root.getiterator():
            element.tag = etree.QName(element).localname
        objectify.deannotate(root, cleanup_namespaces=True)
        return root
