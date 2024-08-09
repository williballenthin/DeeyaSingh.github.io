import yaml
import os
from glob import glob
from datetime import datetime

def render_features(features_list, indent=0):
    rendered = ''
    indent_str = ' ' * indent
    if isinstance(features_list, list):
        for item in features_list:
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, (dict, list)):
                        rendered += f'{indent_str}- {key}:\n'
                        rendered += render_features(value, indent + 2)
                    else:
                        rendered += f'{indent_str}- {key}: {value}\n'
            elif isinstance(item, list):
                rendered += render_features(item, indent)
            else:
                rendered += f'{indent_str}- {item}\n'
    elif isinstance(features_list, dict):
        for key, value in features_list.items():
            if isinstance(value, (dict, list)):
                rendered += f'{indent_str}- {key}:\n'
                rendered += render_features(value, indent + 2)
            else:
                rendered += f'{indent_str}- {key}: {value}\n'
    else:
        rendered += f'{indent_str}- {features_list}\n'
    return rendered

def render_list_item(key, value, indent=0):
    indent_str = ' ' * indent
    rendered = ''
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                for subkey, subvalue in item.items():
                    rendered += render_list_item(subkey, subvalue, indent)
            else:
                rendered += f'{indent_str}  - {item}\n'
    elif isinstance(value, dict):
        for subkey, subvalue in value.items():
            rendered += render_list_item(subkey, subvalue, indent)
    else:
        rendered += f'{indent_str}- {key}: {value}\n'
    return rendered

def get_last_edited_date(file_path):
    last_modified_date = os.path.getmtime(file_path)
    return datetime.fromtimestamp(last_modified_date)

def convert_yaml_to_html(yaml_file, output_dir):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    rule = data.get('rule', {}).get('meta', {})

    namespace = rule.get('namespace', '')
    authors = rule.get('authors', [])
    scope_static = rule.get('scopes', {}).get('static', '')
    scope_dynamic = rule.get('scopes', {}).get('dynamic', '')
    attack = rule.get('att&ck', [])
    mbc = rule.get('mbc', [])
    references = ', '.join(rule.get('references', []))
    examples = rule.get('examples', [])
    features = data.get('rule', {}).get('features', [])
    last_edited = rule.get('last_edited', '')

    if not last_edited:
        last_edited_date = get_last_edited_date(yaml_file)
    else:
        last_edited_date = datetime.strptime(last_edited, '%Y-%m-%d')

    delta = datetime.now() - last_edited_date
    if delta.days < 1:
        last_edited_str = "today"
    elif delta.days == 1:
        last_edited_str = "yesterday"
    elif delta.days < 30:
        last_edited_str = f"{delta.days} days ago"
    elif delta.days < 365:
        last_edited_str = f"{delta.days // 30} months ago"
    else:
        last_edited_str = f"{delta.days // 365} years ago"

    rendered_features = render_features(features)

    name = rule.get('name', 'N/A')
    sanitized_name = name.lower().replace(' ', '-').replace('/', '-').replace('\\', '-')
    html_file_name = f"{sanitized_name}.html"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{name}</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="styles.css">
        <link rel="stylesheet" href="https://deeyasingh.github.io/pagefind/pagefind-ui.css">
        <link rel="stylesheet" href="https://deeyasingh.github.io/pagefind/pagefind-modular-ui.css">
        <link rel="icon" href="https://deeyasingh.github.io/assets/img/favicon.ico" type="image/x-icon">
    </head>
    <body>
        <nav class="navbar navbar-light bg-light justify-content-between">
            <a class="navbar-brand" href="#">
                <img src="https://deeyasingh.github.io/assets/img/logo.png" alt="Logo" style="max-height: 65px;">
            </a>
            <div id="search"></div>
        </nav>
        <section id="showcase">
            <div class="container">
                <h1>{name}</h1>
            </div>
        </section>
        <div class="container">
            <div class="buttons">
                <button>Last edited: {last_edited_str}</button>
            </div>
            <div class="card">
                <div><b>Namespace:</b> {namespace}</div>
                <div><b>Authors:</b></div><div class="grey-box">{render_list_item('Authors', authors)}</div>
                <div><b>Scope:</b></div><div class="grey-box"><b>Static:</b> {scope_static}<br><b>Dynamic:</b> {scope_dynamic}</div>
                <div><b>ATT&CK:</b></div><div class="grey-box">{render_list_item('ATT&CK', attack)}</div>
                <div><b>MBC:</b></div><div class="grey-box">{render_list_item('MBC', mbc)}</div>
                <div><b>References:</b> {references}</div>
                <div><b>Examples:</b></div><div class="grey-box">{render_list_item('Examples', examples)}</div>
                <div><b>Features:</b></div><div class="grey-box">{rendered_features}</div>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        <script src="https://deeyasingh.github.io/pagefind/pagefind-ui.js" type="text/javascript"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                new PagefindUI({{
                    element: "#search",
                    showEmptyFilters: false,
                    excerptLength: 15
                }});
            }});
        </script>
    </body>
    </html>
    """

    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, html_file_name)
    with open(output_file_path, 'w') as html_file:
        html_file.write(html_content)

input_directory = 'capa-rules'
output_directory = 'rules_in_html'
yaml_files = glob(os.path.join(input_directory, '**/*.yml'), recursive=True)

for yaml_file in yaml_files:
    convert_yaml_to_html(yaml_file, output_directory)
