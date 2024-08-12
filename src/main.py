from utils import copy_contents, generate_pages_recursive


copy_contents('static', 'public')
generate_pages_recursive('content', 'template.html', 'public')
