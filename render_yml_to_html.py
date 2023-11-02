import os
import yaml

def convert_yaml_to_html(yaml_file, output_dir):
  
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

  
    rule = data.get('rule', {}).get('meta', {})

    
    namespace = rule.get('namespace', '')
    authors = ', '.join(rule.get('authors', []))
    scope = rule.get('scope', '')
    attack = ', '.join(rule.get('att&ck', []))
    mbc = ', '.join(rule.get('mbc', []))
    references = ', '.join(rule.get('references', []))
    examples = ', '.join(rule.get('examples', []))
    features = data.get('rule', {}).get('features', [])

    
    def render_features(features_list, indent=0):
      rendered = ""
      if not isinstance(features_list, (list, dict)):
          return str(features_list)

      for item in features_list:
          if isinstance(item, dict):
              for key, value in item.items():
                  if isinstance(value, (list, dict)):
                      rendered += " " * indent + "- " + key + ":\n" + render_features(value, indent + 2)
                  else:
                      rendered += " " * indent + "- " + key + ": " + str(value) + "\n"
          elif isinstance(item, list):
              rendered += render_features(item, indent)
          else:
              rendered += " " * indent + "- " + str(item) + "\n"
      return rendered




    features_html = ""
    
    features_html += render_features(features, 4)

   
    html_content = f"""
    <!DOCTYPE html>
<html>
<head>
  <title>{rule.get('name', '')}</title>
  <link rel="stylesheet" type="text/css" href="styles.css">
  <link rel="icon" type="image/png" href="favicon.png">
</head>
<body>
  <header>
    <nav class="navbar bg-body-tertiary">
      <div class="container">
        <a class="navbar-brand" href="index.html">
          <img src="logo.png" alt="CAPA" width="170" height="60">
        </a>
      </div>
    </nav>
  </header>
  
    <div id="rule-name-container">
    <h1 id="rule-name">{rule.get('name', '')}</h1>
    </div>
  <div id="rule-details">
    <p><strong>Namespace:</strong> {namespace}</p>
    <p><strong>Authors:</strong> {authors}</p>
    <p><strong>Scope:</strong> {scope}</p>
    <p><strong>ATT&CK:</strong> {attack}</p>
    <p><strong>MBC:</strong> {mbc}</p>
    <p><strong>References:</strong> {references}</p>
    <p><strong>Examples:</strong> {examples}</p>
    <pre><strong>Features</strong>\n{ features_html }</pre>


  </div>
  <footer>
  </footer>
</body>
</html>"""

    # Save to output directory
    output_file = os.path.join(output_dir, os.path.basename(yaml_file).replace('.yml', '.html'))
    with open(output_file, 'w') as file:
        file.write(html_content)

    

def main():
    input_dir = "assets/data/rules"  
    output_dir = "rules_in_html"  

    for yaml_file in os.listdir(input_dir):
        if yaml_file.endswith('.yml'):
            convert_yaml_to_html(os.path.join(input_dir, yaml_file), output_dir)

if __name__ == "__main__":
    main()
