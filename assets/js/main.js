function showRuleDetails(ruleName) {
  var modifiedRule = ruleName ? ruleName.replace(/\s/g, '-') : '';
  $.get("/assets/data/rules/" + modifiedRule + ".yml", function(data) 
    {
    const ruleStartIndex = data.indexOf('features:');
    const featuresYaml = data.slice(ruleStartIndex);
    const rule = jsyaml.load(data);

    $('#rule-name').text(rule.rule.meta.name);
    $('#rule-details').html(`
      <h2>Details</h2>
      <p><strong>Namespace:</strong> ${rule.rule.meta.namespace}</p>
      <p><strong>Authors:</strong> ${rule.rule.meta.authors.join(', ')}</p>
      <p><strong>Scope:</strong> ${rule.rule.meta.scope ? rule.rule.meta.scope : ''}</p>
      <p><strong>ATT&CK:</strong> ${rule.rule.meta['att&ck'] ? rule.rule.meta['att&ck'].join(', ') : ''}</p>
      <p><strong>MBC:</strong> ${rule.rule.meta.mbc ? rule.rule.meta.mbc.join(', ') : ''}</p>
      <p><strong>References:</strong> ${rule.rule.meta.references ? rule.rule.meta.references.join(', ') : ''}</p>
      <p><strong>Examples:</strong> ${rule.rule.meta.examples ? rule.rule.meta.examples.join(', ') : ''}</p>
      <pre>${featuresYaml}</pre>
    `);
  }, 'text');
}

function onRuleLinkClick(ruleName) {
  event.preventDefault();
  showRuleDetails(ruleName);
}

$(document).ready(function() {
  $('#searchButton').click(function() {
    var selectedNamespace = $('#namespaceSelect').val();
    $('.rule-card').hide(); 
    $('.rule-card').each(function() {
      var ruleNamespace = $(this).data('namespace').split('/')[0];
      if (ruleNamespace == selectedNamespace) {
        $(this).show(); 
      }
    });
  });
});