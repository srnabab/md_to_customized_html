from bs4 import BeautifulSoup
from datetime import datetime
import re
import sys

def parse_and_insert_html(template_path, content_path, output_path):
    try:
        with open(template_path, 'r', encoding='utf-8') as template_file:
            template = template_file.read()

        with open(content_path, 'r', encoding='utf-8') as content_file:
            content = content_file.read()

        template_soup = BeautifulSoup(template, 'html.parser')
        content_soup = BeautifulSoup(content, 'html.parser')

        content_div = template_soup.find(attrs={"class": "content-box"})
        if not content_div:
            raise ValueError("can't find div with class='content-box'")
        
        title_tag = template_soup.new_tag('p', attrs={"class": "title"})
        title_tag.string = content_path.split('.')[0]
        content_div.append(title_tag)

        time_tag = template_soup.new_tag('p', attrs={"class": "time"})
        time_tag.string = datetime.now().strftime("%Y-%m-%d")
        content_div.append(time_tag)

        first_tag = template_soup.new_tag('p', attrs={"class": "first-line"})
        first_tag.string = ""

        markdown_image_pattern = r'!\[(.*?)\](?:\((.*?)\))|!\[\[(.*?)\]\]'
        temp = re.findall(markdown_image_pattern, content)
        matches = []
        if temp != []:
            for match in temp:
                if match[0] or match[1]:
                    matches.append('![' + match[0] + '](' + match[1] + ')')
                elif match[2]:
                    matches.append('![[' + match[2] + ']]')
        else:
            matches.append('![]()')

        print(matches)
        # print(matches.group(0))
        image_index = 0
        first_image_selected = False

        first_p_inserted = False

        for tag in content_soup.find_all():
            if tag.string == None:
                tag.string = ''
            if tag.string == matches[image_index]:
                if not first_image_selected:
                    image_tag = template_soup.new_tag('img', attrs={"class": "first-image"})
                    image_tag['src'] = matches[image_index]
                    image_tag['title'] = matches[image_index]
                    image_tag['alt'] = matches[image_index]
                    content_div.append(image_tag)
                    image_index += 1
                    first_image_selected = True
                else:
                    image_tag = template_soup.new_tag('img')
                    image_tag['src'] = matches[image_index]
                    image_tag['title'] = matches[image_index]
                    image_tag['alt'] = matches[image_index]
                    content_div.append(image_tag)
                    image_index += 1
                continue
            if tag.name == 'img':
                if not first_image_selected:
                    tag['class'] = 'first-image'
                    first_image_selected = True
                content_div.append(tag)
                continue
            # if [child for child in tag.children if isinstance(child, str) == False]:
            #     if tag.find_child().name == 'img':
            #         if not first_image_selected:
            #             tag['class'] = 'first-image'
            #             first_image_selected = True
            #         content_div.append(tag)
            #         continue

            if not first_p_inserted and tag.name == 'p':

                first_tag.string = tag.string
                content_div.append(first_tag)
                first_p_inserted = True
            else:
                content_div.append(tag)
            
        if not first_p_inserted:
            content_div.append(first_tag)

        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(template_soup.encode(formatter='html').decode('utf-8'))

        print(f"Successful: {output_path}")

    except FileNotFoundError as e:
        print(f"can't find: {e}")
    except Exception as e:
        print(f"Error: {e}")

if len(sys.argv) < 2:
    print("Usage: python md_to_page.py <content_path>")
    sys.exit(1)

template_path = "post_template.html"
content_path = sys.argv[1] 
output_path =  sys.argv[1] 

print(f"Processing: {content_path}")

parse_and_insert_html(template_path, content_path, output_path)
