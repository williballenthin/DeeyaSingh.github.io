function showRuleDetails(ruleName) {
  var ruleParam = ruleName.replace(/\s/g, '-');
  $.get("/assets/data/rules/" + ruleParam + ".yml", function(data) {
    // Parse the YAML data using js-yaml
    var ruleData = jsyaml.load(data);
    console.log(ruleData);

    
  });
}

// A function to handle a click on a rule link
function onRuleLinkClick(ruleName) {
  // Prevent the default link behavior
  event.preventDefault();

  // Show the rule details
  showRuleDetails(ruleName);
}

$(document).ready(function() {
  // Event listener for the search button
  $('#searchButton').click(function() {
    var selectedNamespace = $('#namespaceSelect').val();
    $('.rule-card').hide(); // Hide all rule cards initially
    $('.rule-card').each(function() {
      var ruleNamespace = $(this).data('namespace').split('/')[0];
      if (ruleNamespace == selectedNamespace) {
        $(this).show(); // Show only the rule cards with the selected namespace
      }
    });
  });
});

  