from copy_static import copy_static
from generate_page import generate_pages_recursive
def main():
   generate_pages_recursive("./content", "./template.html", "./public")

main()