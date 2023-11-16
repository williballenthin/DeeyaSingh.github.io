require 'yaml'

def convert_yaml_to_html(yaml_file, output_dir)
  data = YAML.load_file(yaml_file)

  rule = data.fetch('rule', {}).fetch('meta', {})

  namespace = rule.fetch('namespace', '')
  authors = rule.fetch('authors', []).join(', ')
  scope = rule.fetch('scope', '')
  attack = rule.fetch('att&ck', []).join(', ')
  mbc = rule.fetch('mbc', []).join(', ')
  references = rule.fetch('references', []).join(', ')
  examples = rule.fetch('examples', []).join(', ')
  features = data.fetch('rule', {}).fetch('features', [])

  def render_features(features_list, indent = 0)
    rendered = ''
    return features_list.to_s unless features_list.is_a?(Enumerable)

    features_list.each do |item|
      if item.is_a?(Hash)
        item.each do |key, value|
          if value.is_a?(Enumerable)
            rendered += ' ' * indent + "- #{key}:\n" + render_features(value, indent + 2)
          else
            rendered += ' ' * indent + "- #{key}: #{value}\n"
          end
        end
      elsif item.is_a?(Enumerable)
        rendered += render_features(item, indent)
      else
        rendered += ' ' * indent + "- #{item}\n"
      end
    end

    rendered
  end

  features_html = render_features(features, 4)

  html_content = <<~HTML
  
  <!DOCTYPE html>
  <html>
  <head>
    <title>#{rule.fetch('name', '')}</title>
    <link rel="stylesheet" type="text/css" href="./styles.css"> <!-- Adjusted path for CSS -->
    <link rel="icon" type="image/png" href="./favicon.png"> <!-- Adjusted path for favicon -->
  </head>
  <body>
    <header>
      <nav class="navbar bg-body-tertiary">
        <div class="container">
          <a class="navbar-brand" href="./index.html"> <!-- Adjusted path for index.html -->
            <img src="./logo.png" alt="CAPA" width="170" height="60"> <!-- Adjusted path for logo.png -->
          </a>
        </div>
      </nav>
    </header>

      <div id="rule-name-container">
        <h1 id="rule-name">#{rule.fetch('name', '')}</h1>
      </div>
      <div id="rule-details">
        <p><strong>Namespace:</strong> #{namespace}</p>
        <p><strong>Authors:</strong> #{authors}</p>
        <p><strong>Scope:</strong> #{scope}</p>
        <p><strong>ATT&CK:</strong> #{attack}</p>
        <p><strong>MBC:</strong> #{mbc}</p>
        <p><strong>References:</strong> #{references}</p>
        <p><strong>Examples:</strong> #{examples}</p>
        <pre><strong>Features</strong>\n#{features_html}</pre>
      </div>
      
    <footer>
    </footer>
    <script>
      var currentUrl = window.location.href;
      var newUrl = currentUrl.replace('/rules_in_html/', '/').replace('.html', '');
      history.replaceState({}, document.title, newUrl);
      </script>
    </body>
    </html>
  HTML
  output_file = File.join(output_dir, File.basename(yaml_file, '.yml') + '.html')
  File.write(output_file, html_content)
end

def main
  input_dir = 'assets/data/rules'
  output_dir = 'rules_in_html'

  Dir.glob(File.join(input_dir, '*.yml')).each do |yaml_file|
    convert_yaml_to_html(yaml_file, output_dir)
  end
end

if __FILE__ == $PROGRAM_NAME
  main
end
