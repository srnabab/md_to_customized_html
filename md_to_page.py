from bs4 import BeautifulSoup
from datetime import datetime
import re
import sys

def parse_and_insert_html(template_path, content_path, output_path):
    try:
        # 读取模板文件
        with open(template_path, 'r', encoding='utf-8') as template_file:
            template = template_file.read()

        # 读取转换后的 HTML 文件
        with open(content_path, 'r', encoding='utf-8') as content_file:
            content = content_file.read()

        # 使用 BeautifulSoup 解析模板和内容
        template_soup = BeautifulSoup(template, 'html.parser')
        content_soup = BeautifulSoup(content, 'html.parser')

        # 找到模板中的目标插入点
        content_div = template_soup.find(attrs={"class": "content-box"})
        if not content_div:
            raise ValueError("模板中未找到 class='content-box' 的 div")
        
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

        # 遍历解析的内容 HTML，将第一个 <p> 替换为带有 class 的 <p>
        first_p_inserted = False

        for tag in content_soup.find_all():  # 使用 find_all 获取所有标签
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

                # 创建一个带有 class 的 <p>
                first_tag.string = tag.string  # 使用原始的文本内容
                content_div.append(first_tag)  # 将新的 <p> 插入模板
                first_p_inserted = True  # 只替换第一个 <p>
            else:
                # 其他内容直接插入
                content_div.append(tag)  # 将其他 <p> 插入模板
            
        if not first_p_inserted:
            content_div.append(first_tag)

        # 将修改后的 HTML 写入输出文件
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(template_soup.encode(formatter='html').decode('utf-8'))

        print(f"成功生成完整的 HTML 页面: {output_path}")

    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

if len(sys.argv) < 2:
    print("Usage: python md_to_page.py <content_path>")
    sys.exit(1)

# 示例使用
template_path = "post_template.html"
content_path = sys.argv[1]  # 转换后的 HTML 文件路径
output_path =  sys.argv[1] # 完整网页的输出路径

print(f"正在处理文件: {content_path}")

parse_and_insert_html(template_path, content_path, output_path)
