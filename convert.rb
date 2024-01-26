require 'yaml'
require 'fileutils'

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

  scope_text = ' ' * 6 + "static: #{rule.fetch('scopes', {}).fetch('static', '')}\n"
  scope_text += ' ' * 6 + "dynamic: #{rule.fetch('scopes', {}).fetch('dynamic', '')}"

  namespace_first_word = Array(rule.fetch('namespace', '')).first.to_s.split('/').first
  namespace = Array(rule.fetch('namespace', '')).first.to_s

  attck_array = Array(rule.fetch('att&ck', ''))

  attack_first_word = attck_array.first.to_s.split('::').first
  attack = attck_array.first.to_s

  mbc_array = Array(rule.fetch('mbc', ''))

  mbc_first_word = mbc_array.first.to_s.split('::').first
  mbc = mbc_array.first.to_s

  scopes_static = rule.fetch('scopes', {}).fetch('static', '')
  scopes_dynamic = rule.fetch('scopes', {}).fetch('dynamic', '')

  scope = rule.fetch('scope', '')
  authors = Array(rule.fetch('authors', [])).map { |author| author.downcase }
  references = rule.fetch('references', []).join(', ')
  examples = rule.fetch('examples', []).join(', ')

  namespace_filters = "<span data-pagefind-filter=\"namespace: #{namespace_first_word}\"></span>" unless namespace.to_s.empty?
  attack_filters = "<span data-pagefind-filter=\"ATT&CK: #{attack_first_word}\"></span>" unless attack.to_s.empty?
  mbc_filters = "<span data-pagefind-filter=\"MBC: #{mbc_first_word}\"></span>" unless mbc.to_s.empty?

  scope_filters = ''
  scope_filters += "<span data-pagefind-filter=\"scope(static): #{scopes_static}\"></span>" unless scopes_static.to_s.empty?
  scope_filters += "<span data-pagefind-filter=\"scope(dynamic): #{scopes_dynamic}\"></span>" unless scopes_dynamic.to_s.empty?

  html_content = <<~HTML
  ---
  permalink: "/#{rule.fetch('name', '').gsub(' ', '-').downcase}/"
  ---

  <!DOCTYPE html>
  <html>
  <head>
    <title>#{rule.fetch('name', '')}</title>
    <link rel="stylesheet" type="text/css" href="{{ "assets/styles.css" | relative_url }}">
    <link rel="icon" type="image/png"  href="{{ "assets/img/favicon.png" | relative_url }}"  > 
    <link data-pagefind-meta="url[href]" rel="canonical" href="/#{rule.fetch('name', '').gsub(' ', '-').downcase}/">
  </head>
  <body>
    <header>
      <nav class="navbar bg-body-tertiary">
        <div class="container">
          <a class="navbar-brand" href="{{ "/" | relative_url }}">
            <img src="{{ "assets/img/logo.png" | relative_url }}" alt="CAPA" width="170" height="60">
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
      <pre><strong>Scope:</strong>\n#{scope_text}</pre>
      <p><strong>ATT&CK:</strong> #{attack}</p>
      <p><strong>MBC:</strong> #{mbc}</p>
      <p><strong>References:</strong> #{references}</p>
      <p><strong>Examples:</strong> #{examples}</p>
      <pre><strong>Features</strong>\n#{features_html}</pre>
    </div>
    #{namespace_filters}  
    #{attack_filters} 
    #{mbc_filters}
    #{scope_filters}
    #{authors.map { |author| "<span data-pagefind-filter=\"author: #{author}\"></span>" }.join("\n")}
    <footer>
    </footer>
  </body>
  </html>
  HTML

  output_file = File.join(output_dir, File.basename(yaml_file, '.yml') + '.html')
  File.write(output_file, html_content)
end

def main
  # Convert YAML to HTML
  input_dir = '_data/rules'  # Change the input directory to 'capa-rules'
  output_dir = 'rules_in_html'
  Dir.glob(File.join(input_dir, '*.yml')).each do |yaml_file|
    convert_yaml_to_html(yaml_file, output_dir)
  end

  # Write individual YAML files
  capa_rules_path = "capa-rules"
  output_folder = "_data/rules"
  FileUtils.mkdir_p(output_folder)
  yaml_files = Dir[File.join(capa_rules_path, '**/*.yml')]

  yaml_files.each_with_index do |file_path, index|
    rule_data = YAML.safe_load(File.read(file_path))
    rule_name = File.basename(file_path, ".yml")
    filename = "#{rule_name.downcase.gsub(' ', '_')}.yml"
    output_file_path = File.join(output_folder, filename)
    File.open(output_file_path, 'w') do |file|
      file.puts YAML.dump(rule_data)
    end
  end

  puts "Individual YAML files written to #{output_folder}"
end

if __FILE__ == $PROGRAM_NAME
  main
end
