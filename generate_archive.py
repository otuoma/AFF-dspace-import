import os.path
import time

import pandas
import utilities


utils = utilities.Utils()

def read_csv():

    df = pandas.read_csv('publications_export.csv', parse_dates=['post_date'])
    counter = 1
    for index, row in df.iterrows():

        print(f"Processing {counter} - id {row['id']}")

        item_id = row['id']

        item_dir = utils.create_item_dir(item_id=item_id)
        metadata = utils.create_xml_file(metadata=row)

        # bitstreams
        if "english_upload" in row.keys():
            english_bitstream = utils.download_bitstream(item_id, row['english_upload'], "english_")

            with open(f"{item_dir}/contents", "+a") as f:
                if english_bitstream:
                    f.write(f"english_{item_id}.pdf")

        if "french_upload" in row.keys():
            french_bitstream = utils.download_bitstream(row['id'], row['french_upload'], "french_")
            with open(f"{item_dir}/contents", "+a") as f:
                if french_bitstream:
                    f.write(f"\nfrench_{item_id}.pdf")

        # # collections
        with open(f"{item_dir}/collections", "w") as f:
            collection_id = utils.get_collection_id(row["Publication_Type"])
            if collection_id:
                # handle of collection to which to save the item
                collection_handle = f"2367-AFF/{collection_id}"
                f.write(collection_handle)

        counter += 1
        print(" - Sleeping for 2 secs before resuming job ...")

        time.sleep(2)

read_csv()