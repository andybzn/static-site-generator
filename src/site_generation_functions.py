import os
import re
import shutil
from src.markdown_conversion_functions import markdown_to_html_node


def copy_static_files(source_filepath, destination_filepath):
    """Purges the target filepath, then recursively copies files from the
    provided source filepath to that location

    :param source_filepath: The source directory to copy
    :type source_filepath: str
    :param destination_filepath: The target directory
    :type destination_filepath: str
    :returns: Nothing
    :rtype: None
    """
    # Purge the destination_filepath and create a new directory
    if os.path.exists(destination_filepath):
        shutil.rmtree(destination_filepath)
    os.mkdir(destination_filepath)

    # Recursively copy files to the destination directory
    for file in os.listdir(source_filepath):
        source_file = os.path.join(source_filepath, file)
        destination_file = os.path.join(destination_filepath, file)
        print(f"copying: {source_file} -> {destination_file}")
        if os.path.isfile(source_file):
            shutil.copy(source_file, destination_file)
        else:
            copy_static_files(source_file, destination_file)


def extract_title(markdown):
    """Takes a markdown formatted string and returns the h1 heading text.
    This function will raise an exception if no valid heading is found.

    :param markdown: A markdown formatted string
    :type markdown: str
    :returns: The title text of the markdown document
    :rtype: str
    """
    pattern = re.compile(r"^#\s(?P<title>.*)")
    matches = pattern.search(markdown)
    if matches is None:
        raise ValueError("No valid heading 1 found in markdown")
    return matches.group("title")


def write_destination(filepath, content):
    """Takes a filepath and content string, and writes the content to that filepath

    :param filepath: The path to the destination file
    :type filepath: str
    :param content: The content to write
    :type content: str
    :returns: Nothing
    :rtype: None
    """
    path_parts = filepath.split("/")
    if len(path_parts) > 1:
        os.makedirs("/".join(path_parts[:-1]), exist_ok=True)
    with open(filepath, "w") as destination_file:
        destination_file.write(content)


def generate_page(source_filepath, template_path, destination_filepath):
    """Generate a html page from a source markdown file, using a template html file.
    Writes the file to the destination filepath.

    :param source_filepath: The filepath of the source markdown file
    :type source_filepath: str
    :param template_path: The path to the template file used to generate the html document
    :type template_path: str
    :param destination_filepath: The filepath to write the html file to
    :type destination_filepath: str
    :returns: Nothing
    :rtype: None
    """
    print(
        f"generating page: {
            source_filepath} -> {destination_filepath} using {template_path}"
    )
    markdown_content = open(source_filepath, "r").read()
    template_content = open(template_path, "r").read()
    html_content = markdown_to_html_node(markdown_content).to_html()
    html_markup = template_content.replace(
        " {{ Title }} ", extract_title(markdown_content)
    ).replace("{{ Content }}", html_content)

    write_destination(destination_filepath, html_markup)


def generate_pages_recursive(content_dir_path, template_path, dest_dir_path):
    """Generate html pages from a directory of markdown files. This function will
    recursively process subdirectories.

    :param content_dir_path: The directory containing the site content
    :type content_dir_path: str
    :param template_path: The path to the template file used to generate the site
    :type template_path: str
    :param dest_dir_path: The directory to write the site content to
    :type dest_dir_path: str
    :returns: Nothing
    :rtype: None
    """
    for leaf in os.listdir(content_dir_path):
        leaf_filepath = os.path.join(content_dir_path, leaf)
        if os.path.isfile(leaf_filepath):
            target_filepath = os.path.join(dest_dir_path, leaf.replace(".md", ".html"))
            generate_page(leaf_filepath, template_path, target_filepath)
        else:
            target_filepath = os.path.join(dest_dir_path, leaf)
            generate_pages_recursive(leaf_filepath, template_path, target_filepath)
