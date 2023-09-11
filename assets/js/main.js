$(document).ready(function() {
  function showRuleDetails(ruleName) {
      var modifiedRule = ruleName ? ruleName.replace(/\s/g, '-') : '';
      $.get("/assets/data/rules/" + modifiedRule + ".yml", function(data) {
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

  function onRuleLinkClick(event, ruleName) {
      event.preventDefault();
      showRuleDetails(ruleName);
  }

  $('.metadata-values').hide();

  $('#metadataSelect').change(function() {
      $('.metadata-values').hide();
      const selectedMetadata = $(this).val();
      $('#' + selectedMetadata + 'Values').show();
  });

  $('#searchButton').click(function() {
    const selectedMetadata = $('#metadataSelect').val();
    const selectedValueDropdownId = selectedMetadata + 'Values';
    const selectedValue = $('#' + selectedValueDropdownId).val();
    
    console.log(`Filtering on [${selectedMetadata}] with value [${selectedValue}]`);

    $('.rule-card').hide();

    if (selectedMetadata && selectedValue) {
        
        if (selectedMetadata === 'author') {

            $('.rule-card').each(function() {

                const authorContent = $(this).find('.card-author').text();
                if (authorContent.includes(selectedValue)) {
                    $(this).show();
                }
            });

        } else if (selectedMetadata === "namespace") {
            $(`.rule-card[data-${selectedMetadata}^="${selectedValue}"]`).show();

        } else if (selectedMetadata === "mbc") {
          $(`.rule-card[data-${selectedMetadata}*="${selectedValue}"]`).show();
        } else if (selectedMetadata === "attck") {
            $(`.rule-card[data-attck*="${selectedValue}"]`).show();
        } else {
            $(`.rule-card[data-${selectedMetadata}="${selectedValue}"]`).show();
        }

    } else {
        $('.rule-card').show();  
    }
});
});
