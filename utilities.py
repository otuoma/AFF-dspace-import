import os
import requests
import xml.etree.ElementTree as et
from xml.dom import minidom


class Utils:

    def create_xml_file(self, metadata):

        root = et.Element("dublin_core")
        root.set("schema", "dc")

        # title
        title_el = et.Element("dcvalue")
        title_el.text = str(metadata['Title'])
        title_el.set("element", "title")
        root.append(title_el)

        # contributor
        contributor_el = et.Element("dcvalue")
        contributor_el.text = str(metadata['author'])
        contributor_el.set("element", "contributor")
        contributor_el.set("qualifier", "author")
        root.append(contributor_el)

        # date available
        date_avail_el = et.Element("dcvalue")
        date_avail_el.text = str(metadata['post_date'])
        date_avail_el.set("element", "date")
        date_avail_el.set("qualifier", "available")
        root.append(date_avail_el)

        # abstract
        abstract_el = et.Element("dcvalue")
        abstract_el.text = str(metadata['Abstract'])
        abstract_el.set("element", "description")
        abstract_el.set("qualifier", "abstract")
        root.append(abstract_el)

        # publisher
        publisher_el = et.Element("dcvalue")
        publisher_el.text = "African Forest Forum (AFF)"
        publisher_el.set("element", "publisher")
        publisher_el.set("qualifier", "none")
        root.append(publisher_el)

        # type
        type_el = et.Element("dcvalue")
        type_el.text = str(metadata["Publication_Type"])
        type_el.set("element", "type")
        type_el.set("qualifier", "none")
        root.append(type_el)

        tree = et.ElementTree(root)
        with open(f"aff_archive/item_{metadata['id']}/dublin_core.xml", "wb") as f:
            try:
                tree.write(f, encoding="utf-8", xml_declaration=True, default_namespace=None)
            except Exception as e:
                print("====================================================")
                print(f" - Failed saving metadata file for {metadata['id']}, Error => {e}")
                print("====================================================")

    def download_bitstream(self, item_id: int, download_url: str, language_prefix: str) -> bool:

        print(f" - Attempting to download {download_url}")
        status = False

        try:
            resp = requests.get(download_url)
            file_location = f"aff_archive/item_{item_id}/{language_prefix}{item_id}.pdf"
            with open(file_location, "wb") as f:
                f.write(resp.content)
            print(f" - Saved file to {file_location}")
            status = True

        except Exception as e:
            print(f" - Download failed: {e}")

        return status

    def create_item_dir(self, item_id: int) -> str:

        dir_path = f"aff_archive/item_{item_id}"
        print(f" - Attempting to create {dir_path}")
        if not os.path.exists(dir_path):
            try:
                os.mkdir(dir_path)
                print(" - Created")
            except Exception as e:
                print(f" - Failed creating item dir => {dir_path}: {e}")
        else:
            print(f" - {dir_path} already exists")

        return dir_path

    def get_collection_id(self, publication_type: str) -> int:

        collections = {
            "Book": 226,
            "Compendium": 227,
            "Factsheet": 228,
            "Journal Article": 229,
            "Newsletter": 230,
            "Policy Brief": 231,
            "Proceedings": 232,
            "Report": 233,
            "Training Module": 234,
            "Working Paper": 235
        }
        if publication_type in collections:
            return collections.get(publication_type)
        else:
            print(f" - Publication type: {publication_type} does not exist on dspace")
