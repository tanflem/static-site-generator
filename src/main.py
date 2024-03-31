from textnode import TextNode
import os
import shutil


# ASSIGNMENT
# Create a generate_pages_recursive(dir_path_content, template_path, dest_dir_path) function. It should crawl every entry in the dir_path_content directory and generate a new .html page for each markdown file it finds. The generated pages should be written to the dest_dir_path directory using the template_path template.

# Helpful docs:

# os.listdir
# os.path.join
# os.path.isfile
# pathlib.Path
# Next, change your main function to use generate_pages_recursive instead of generate_page. You should generate a page for every markdown file in the content directory and write the results to the public directory.

# Finally, update your content directory:

# Move the index.md file to a new directory called majesty, and create a new top-level index.md:

# # Tolkien Fan Club

# I like Tolkien. Read my [first post here](/majesty)
# Copy icon
# Run your server again and check out the new site. You should see a link to your new majesty page. Paste the root URL of your site into the textbox and submit the results.

# You're done! Feel free to change the content to your heart's content, you've built a static site generator from scratch!
def generate_pages_recursive(dir_content, template_path, dest_dir):
    for item in os.listdir(dir_content):
        path = os.path.join(dir_content, item)
        if os.path.isfile(path) and path.endswith(".md"):
            generate_page(path, template_path, os.path.join(dest_dir, item.replace(".md", ".html")))
        elif os.path.isdir(path):
            generate_pages_recursive(path, template_path, os.path.join(dest_dir, item))


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")

def generate_page(from_path, template_path, to_path):
    print(f"Generating {to_path} to {from_path} using {template_path}")
    markdown = open(from_path).read()
    nodes = TextNode.markdown_to_html_node(markdown)
    title = extract_title(markdown)

    template = open(template_path).read()
    html = template.replace(r"{{ Content }}", nodes.to_html())
    html = html.replace(r"{{ Title }}", title)
    
    to_dir = os.path.dirname(to_path)
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)

    open(to_path, "w").write(html)


def copy_static(directory = "static", target = "public"):
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        target_path = os.path.join(target, item)
        if os.path.isfile(path):
            shutil.copy(path, target_path)
            print(f"Copying {path} to {target_path}")
        else:
            copy_static(path, target_path)

def main():
    copy_static()
    generate_pages_recursive("content", "template.html", "public")

main()