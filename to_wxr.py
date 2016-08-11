# encoding: utf8

"""
Create Disqus-importable XML file
from blog posts and comments
"""

from lxml import etree
import os
from pprint import pprint
import json
from datetime import datetime

path = "export"

def init_xml():
    """Create an etree XML document"""
    data = '''<?xml version="1.0" encoding="UTF-8"?>
      <rss version="2.0"
      xmlns:content="http://purl.org/rss/1.0/modules/content/"
      xmlns:dsq="http://www.disqus.com/"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:wp="http://wordpress.org/export/1.0/">
      <channel></channel></rss>'''
    xml = etree.fromstring(data)
    return xml

if __name__ == "__main__":
    tree = init_xml()
    channel = tree.find("channel")

    for post_id in os.listdir(path):
        subdir = "/".join((path, post_id))
        post_file = "%s/post_%s.json" % (subdir, post_id)
        
        if not os.path.exists(post_file):
            continue
        
        # read JSON file
        post = None
        with open(post_file, "rb") as jsonfile:
            post = json.load(jsonfile)

        #pprint(post)

        item = etree.SubElement(channel, "item")

        # item attributes
        title = etree.SubElement(item, "title")
        title.text = post["name"]

        link = etree.SubElement(item, "link")
        link.text = post["published_url"]

        creator = etree.SubElement(item, "{http://purl.org/dc/elements/1.1/}creator")
        creator.text = post["blog_author"]["full_name"]
            
        content = etree.SubElement(item, "{http://purl.org/rss/1.0/modules/content/}encoded")
        content.text = etree.CDATA("")
        if post["post_body"] is not None:
            content.text = etree.CDATA(post["post_body"])

        # This remains empty
        thread_id = etree.SubElement(item, "{http://www.disqus.com/}thread_identifier")
        thread_id.text = post["slug"]
        
        wp_post_date = etree.SubElement(item, "{http://wordpress.org/export/1.0/}post_date_gmt")
        wp_post_date.text = datetime.fromtimestamp(post["publish_date"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        
        wp_comment_status = etree.SubElement(item, "{http://wordpress.org/export/1.0/}comment_status")
        wp_comment_status.text = "open"
        
        comment_dir = "%s/comments" % subdir
        
        if os.path.exists(comment_dir):
            
            for comment_file in os.listdir(comment_dir):
                comment_path = "%s/%s" % (comment_dir, comment_file)
                print(comment_path)
                with open(comment_path, "rb") as jsonfile:
                    comment_data = json.load(jsonfile)
                # for every comment
                comment = etree.SubElement(item, "{http://wordpress.org/export/1.0/}comment")

                comment_id = etree.SubElement(item, "{http://wordpress.org/export/1.0/}comment_id")
                comment_id.text = str(comment_data["id"])

                comment_author = etree.SubElement(item, "{http://wordpress.org/export/1.0/}comment_author")
                comment_author.text = comment_data["userName"]
                
                comment_author_email = etree.SubElement(item, "{http://wordpress.org/export/1.0/}comment_author_email")
                comment_author_email.text = comment_data["userEmail"]
                
                comment_date_gmt = etree.SubElement(item, "{http://wordpress.org/export/1.0/}comment_date_gmt")
                comment_date_gmt.text = datetime.fromtimestamp(comment_data["createdAt"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                
                comment_author_url = etree.SubElement(item, "{http://wordpress.org/export/1.0/}comment_author_url")
                if comment_data["userUrl"] is not None:
                    comment_author_url.text = comment_data["userUrl"]
                
                comment_author_ip = etree.SubElement(item, "{http://wordpress.org/export/1.0/}comment_author_IP")
                if comment_data["userIp"] is not None:
                    comment_author_ip.text = comment_data["userIp"]

                comment_content = etree.SubElement(item, "{http://wordpress.org/export/1.0/}comment_content")
                comment_content.text = etree.CDATA(comment_data["comment"])
                
                comment_approved = etree.SubElement(item, "{http://wordpress.org/export/1.0/}comment_approved")
                if comment_data["state"] == "APPROVED":
                    comment_approved.text = "1"
                else:
                    comment_approved.text = "0"
                
                comment_parent = etree.SubElement(item, "{http://wordpress.org/export/1.0/}comment_parent")
                if comment_data["parent"]["id"] != 0:
                    comment_parent.text = str(comment_data["parent"]["id"])

    f = open("disqus.xml", "wb")
    f.write(etree.tostring(tree, pretty_print=True))
    f.close()
