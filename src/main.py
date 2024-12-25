from src.site_generation_functions import copy_static_files, generate_pages_recursive


def main():
    """Kicks off the generation of the static site.

    :returns: Nothing
    :rtype: None
    """
    copy_static_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
