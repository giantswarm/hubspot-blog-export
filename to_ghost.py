# encoding: utf8

"""
Create Ghost-importable XML file
from blog posts and comments
"""

import os
from pprint import pprint
import json
from datetime import datetime
import time

path = "export"


if __name__ == "__main__":

    out = {
        "meta": {
            "exported_on": time.time(),
            "version": "003"
        },
        "data": {
            "posts": [],
            "tags": [],
            "posts_tags": [],
            "users": [],
            "roles_users": []
        }
    }
    
    for post_id in os.listdir(path):
        subdir = "/".join((path, post_id))
        post_file = "%s/post_%s.json" % (subdir, post_id)
        
        if not os.path.exists(post_file):
            continue
        
        # read JSON file
        post = None
        with open(post_file, "rb") as jsonfile:
            post = json.load(jsonfile)

        out_post = {
            "id": post["id"],
            "title": post["name"],
            "slug": post["slug"],
            "markdown": post["post_body"],
            "html": post["post_body"],
            "image": None,
            "featured": 0,
            "page": 0,
            "status": "published",
            "language": "en_US",
            "meta_title": None,
            "meta_description": post["meta_description"],
            "author_id": 1,
            "created_at": post["created"],
            "created_by": 1,
            "updated_at": post["publish_date"],
            "updated_by": 1,
            "published_at": post["publish_date"],
            "published_by": 1
        }
        
        out["data"]["posts"].append(out_post)
        

    f = open("ghost.json", "wb")
    f.write(json.dumps(out, indent=2, sort_keys=True))
    f.close()
