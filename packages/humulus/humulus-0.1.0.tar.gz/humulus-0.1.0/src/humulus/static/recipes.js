/*
  Copyright 2019 Mike Shoup

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/

// Calculate percentage and background color for display functions
function calculatePct(value, low, high) {
  var pct = Math.round(100 * (value-low )/ (high - low));
  var color = 'bg-success';
  if (pct > 85) {
    color = 'bg-danger';
    if (pct > 100) {
      pct = 100;
    }
  } else if (pct <=15 ) {
    color = 'bg-warning';
    if (pct <= 0) {
      pct = 5; // We want a little bit of bar showing
    }
  }

  return {pct: pct, color: color};
}

// unbinds and re-binds the change event
function rebindChangeEvents() {
  $('.ingredient-field').unbind('change');
  $('.ingredient-field').change(displayAll);
}

// Correct all the indices for forms matching item.
function adjustIndices(removedIndex, item) {
  var $forms = $(item);
  $forms.each(function(i) {
    var $form = $(this);
    var index = parseInt($form.data('index'));
    var newIndex = index - 1;
    if (index <= removedIndex) {
      // Skip this one
      return true;
    }

    // Change form index
    $form.data('index', newIndex);

    // Change ID in form input, select, and labels
    $form.find('input').each(function(j) {
      var $item = $(this)
      $item.attr('id', $item.attr('id').replace(index, newIndex));
      $item.attr('name', $item.attr('name').replace(index, newIndex));
    });
    $form.find('select').each(function(j) {
      var $item = $(this)
      $item.attr('id', $item.attr('id').replace(index, newIndex));
      $item.attr('name', $item.attr('name').replace(index, newIndex));
    });
  });
}

// Remove a subform from a form matching `formClass` closest to `$remButton`.
// Adjust length on element matching `formsId`. Also adjust indices.
function removeForm($remButton, formClass, formsId) {
  var $removedForm = $remButton.closest(formClass);
  var removedIndex = parseInt($removedForm.data('index'));
  $removedForm.remove();
  var $fermsDiv = $(formsId);
  $fermsDiv.data('length', $fermsDiv.data('length') - 1);
  adjustIndices(removedIndex, formClass);
  displayAll();
}

// Remove a fermentable
function removeFerm() {
  removeForm($(this), '.ferm-form', '#ferms');
}

// Remove a hop
function removeHop() {
  removeForm($(this), '.hop-form', '#hops');
}

// Remove a mash step
function removeMashStep() {
  removeForm($(this), '.mash-form', '#mash');
}

// Add a fermentable
function addFerm() {
  var $fermsDiv = $('#ferms');
  var fermsLength = $fermsDiv.data('length');
  if (fermsLength == 20) {
    window.alert("Can't have more than 20 fermentables.");
    return;
  }
  var newFerm = `<div class="border pl-2 pr-2 pt-1 pb-1 ferm-form" data-index="${fermsLength}">` +
                // Name field
                '<div class="row"><div class="col"><div class="form-group">' +
                `<label for="fermentables-${fermsLength}-name">Name</label>` +
                `<input class="form-control form-control-sm ingredient-field" id="fermentables-${fermsLength}-name"` +
                ` name="fermentables-${fermsLength}-name" required type="text" value="">` +
                '</div></div></div>' + // End name field
                '<div class="row">' +
                // Type field
                '<div class="col-sm"><div class="form-group">' +
                `<label for="fermentables-${fermsLength}-type">Type</label>` +
                `<select class="custom-select custom-select-sm ingredient-field" id="fermentables-${fermsLength}-type"` +
                ` name="fermentables-${fermsLength}-type" required>` +
                '<option value="Grain">Grain</option>' +
                '<option value="LME">LME</option>' +
                '<option value="DME">DME</option>' +
                '<option value="Sugar">Sugar</option>' +
                '<option value="Non-fermentable">Non-fermentable</option>' +
                '<option value="Other">Other</option></select>' +
                '</div></div>' + // End type field
                // Amount field
                '<div class="col-sm"><div class="form-group">' +
                `<label for="fermentables-${fermsLength}-amount">Amount (lb)</label>` +
                `<input class="form-control form-control-sm ingredient-field" id="fermentables-${fermsLength}-amount"` +
                ` name="fermentables-${fermsLength}-amount" required type="text" value="">` +
                '</div></div>' + // End amount field
                // PPG field
                '<div class="col-sm"><div class="form-group">' +
                `<label for="fermentables-${fermsLength}-ppg">PPG</label>` +
                `<input class="form-control form-control-sm ingredient-field" id="fermentables-${fermsLength}-ppg"` +
                ` name="fermentables-${fermsLength}-ppg" required type="text" value="">` +
                '</div></div>' + // End PPG field
                // Color field
                '<div class="col-sm"><div class="form-group">' +
                `<label for="fermentables-${fermsLength}-color">Color (°L)</label>` +
                `<input class="form-control form-control-sm ingredient-field" id="fermentables-${fermsLength}-color"` +
                ` name="fermentables-${fermsLength}-color" required type="text" value="">` +
                '</div></div>' + // End PPG field
                '</div>' +
                // Remove button
                '<div class="row"><div class="col">' +
                '<button type="button" class="float-right btn btn-sm btn-outline-danger rem-ferm">' +
                'Remove fermentable</button>' +
                '</div></div>' + // End remove button
                '</div>';
  $fermsDiv.append(newFerm);
  $fermsDiv.data('length', fermsLength + 1);
  // Unbind click events and re-bind them. This is needed to prevent multiple click events
  $('.rem-ferm').unbind('click');
  $('.rem-ferm').click(removeFerm);
  rebindChangeEvents();
}

// Add a hop
function addHop() {
  var $hopsDiv = $('#hops');
  var hopsLength = $hopsDiv.data('length');
  if (hopsLength == 20) {
    window.alert("Can't have more than 20 hops.");
    return;
  }

  var newHop =  `<div class="border pl-2 pr-2 pt-1 pb-1 hop-form" data-index="${hopsLength}">` +
                // Name field
                '<div class="row"><div class="col"><div class="form-group">' +
                `<label for="hops-${hopsLength}-name">Name</label>` +
                `<input class="form-control form-control-sm ingredient-field" id="hops-${hopsLength}-name"` +
                ` name="hops-${hopsLength}-name" required type="text" value="">` +
                '</div></div></div>' + // End name field
                '<div class="row">' +
                // Usage field
                '<div class="col-sm"><div class="form-group">' +
                `<label for="hops-${hopsLength}-use">Usage</label>` +
                `<select class="custom-select custom-select-sm ingredient-field" id="hops-${hopsLength}-use"` +
                ` name="hops-${hopsLength}-use" required>` +
                '<option value="Boil">Boil</option>' +
                '<option value="FWH">FWH</option>' +
                '<option value="Whirlpool">Whirlpool</option>' +
                '<option value="Dry-Hop">Dry-Hop</option></select>' +
                '</div></div>' + // End usage field
                // Alpha acid % field
                '<div class="col-sm"><div class="form-group">' +
                `<label for="hops-${hopsLength}-alpha">Alpha Acid %</label>` +
                `<input class="form-control form-control-sm ingredient-field" id="hops-${hopsLength}-alpha"` +
                ` name="hops-${hopsLength}-alpha" required type="text" value="">` +
                '</div></div>' + // End alpha acid % field
                // Duration field
                '<div class="col-sm"><div class="form-group">' +
                `<label for="hops-${hopsLength}-duration">Duration (min/day)</label>` +
                `<input class="form-control form-control-sm ingredient-field" id="hops-${hopsLength}-duration"` +
                ` name="hops-${hopsLength}-duration" required type="text" value="">` +
                '</div></div>' + // End duration field
                // Amount field
                '<div class="col-sm"><div class="form-group">' +
                `<label for="hops-${hopsLength}-amount">Amount (oz)</label>` +
                `<input class="form-control form-control-sm ingredient-field" id="hops-${hopsLength}-amount"` +
                ` name="hops-${hopsLength}-amount" required type="text" value="">` +
                '</div></div>' + // End amount field
                '</div>' +
                // Remove button
                '<div class="row"><div class="col">' +
                '<button type="button" class="float-right btn btn-sm btn-outline-danger rem-hop">' +
                'Remove Hop</button>' +
                '</div></div>' + // End remove button
                '</div>';

  $hopsDiv.append(newHop);
  $hopsDiv.data('length', hopsLength + 1);
  // Unbind click events and re-bind them. This is needed to prevent multiple click events
  $('.rem-hop').unbind('click');
  $('.rem-hop').click(removeHop);
  rebindChangeEvents();
}

// Add a new mash step
function addMashStep() {
  var $mashDiv = $('#mash');
  var stepsLength = $mashDiv.data('length');
  if (stepsLength == 20) {
    window.alert("Can't have more than 20 mash steps.");
    return;
  }

  var newStep = `<div class="border pl-2 pr-2 pt-1 pb-1 mash-form" data-index="${stepsLength}">` +
                '<div class="row"><div class="col-sm-8"><div class="form-group">' +
                // Step Name Field
                `<label for="mash-steps-${stepsLength}-name">Step Name</label>` +
                `<input class="form-control form-control-sm" id="mash-steps-${stepsLength}-name" ` +
                `name="mash-steps-${stepsLength}-name" required type="text" value="">` +
                '</div></div>' + // End Step Name field
                // Type field
                '<div class="col-sm-4"><div class="form-group">' +
                `<label for="mash-steps-${stepsLength}-type">Type</label>` +
                `<select class="custom-select custom-select-sm" id="mash-steps-${stepsLength}-type" ` +
                `name="mash-steps-${stepsLength}-type">` +
                '<option value="Infusion">Infusion</option>' +
                '<option value="Temperature">Temperature</option>' +
                '<option value="Decoction">Decoction</option></select>' +
                '</div></div></div>' + // End Type field
                // Temperature field
                '<div class="row"><div class="col-sm"><div class="form-group">' +
                `<label for="mash-steps-${stepsLength}-temp">Temperature (°F)</label>` +
                `<input class="form-control form-control-sm" id="mash-steps-${stepsLength}-temp" ` +
                `name="mash-steps-${stepsLength}-temp" required type="text" value="">` +
                '</div></div>' + // End temperature field
                //Time field
                '<div class="col-sm"><div class="form-group">' +
                `<label for="mash-steps-${stepsLength}-time">Time (min)</label>` +
                `<input class="form-control form-control-sm" id="mash-steps-${stepsLength}-time" ` +
                `name="mash-steps-${stepsLength}-time" required type="text" value="">` +
                '</div></div>' + // End time field
                // Amount field
                '<div class="col-sm"><div class="form-group">' +
                `<label for="mash-steps-${stepsLength}-amount">Water Amount (gal)</label>` +
                `<input class="form-control form-control-sm" id="mash-steps-${stepsLength}-amount" ` +
                `name="mash-steps-${stepsLength}-amount" type="text" value="">` +
                '</div></div></div>' + // End amount field
                '<div class="row"><div class="col">' +
                '<button type="button" class="float-right btn btn-sm btn-outline-danger rem-step">Remove Step</button>' +
                '</div></div></div>';

  $mashDiv.append(newStep);
  $('.rem-step').unbind('click');
  $('.rem-step').click(removeMashStep);
}

// Calculate recipe's original gravity
function calculateOG() {
  var fermsLength = $('#ferms').data('length');
  if (fermsLength == 0) {
    return 0;
  }
  var points = 0;
  var grain_points = 0;
  for (var i = 0; i < fermsLength; i++) {
    var ppg = parseFloat($(`#fermentables-${i}-ppg`).val()) || 0.0;
    var amt = parseFloat($(`#fermentables-${i}-amount`).val()) || 0.0;

    // Check if type is grain
    if ($(`#fermentables-${i}-type`).val() == 'Grain') {
      grain_points += ppg * amt;
    } else {
      points += ppg * amt;
    }
  }
  // Add grain_points to points, adjusting for efficiency
  var efficiency = parseFloat($(`#efficiency`).val()) || 0;
  var volume = parseFloat($(`#volume`).val()) || 0;
  points += grain_points * efficiency / 100;
  return 1 + points / (1000 * volume);
}

// display OG
function displayOG(data) {
  var og = calculateOG().toFixed(3);
  if (data !== null) {
    var result = calculatePct(og, data.og.low, data.og.high)
    $('#estimated-og').html(`<div class="progress spec-progress"><div class="progress-bar ${result.color}" ` +
      `role="progressbar" style="width: ${result.pct}%;" aria-valuenow="${og}" aria-valuemin="${data.og.low}" ` +
      `aria-valuemax="${data.og.high}">${og}</div></div>`);
  } else {
    $('#estimated-og').text(og);
  }
}

// Calculate final gravity
function calculateFG() {
  var fermsLength = $('#ferms').data('length');
  if (fermsLength == 0) {
    return 0;
  }

  var og = parseFloat(calculateOG()) || 0.0;
  var og_delta = 0.0;
  var volume = parseFloat($(`#volume`).val()) || 0;
  for (var i = 0; i < fermsLength; i++) {
    if ($(`#fermentables-${i}-type`).val() == 'Non-fermentable') {
      var ppg = parseFloat($(`#fermentables-${i}-ppg`).val()) || 0.0;
      var amt = parseFloat($(`#fermentables-${i}-amount`).val()) || 0.0;
      og_delta += amt * ppg / (volume * 1000)
    }
  }

  var low_attenuation = parseFloat($('#yeast-low_attenuation').val()) || 0.0;
  var high_attenuation = parseFloat($('#yeast-high_attenuation').val()) || 0.0;
  var attenuation = (low_attenuation + high_attenuation) / 200;
  return 1 + (og - 1 - og_delta)*(1 - attenuation) + og_delta;
}

// Display FG
function displayFG(data) {
  var fg = calculateFG().toFixed(3);
  if (data !== null) {
    var result = calculatePct(fg, data.fg.low, data.fg.high)
    $('#estimated-fg').html(`<div class="progress spec-progress"><div class="progress-bar ${result.color}" ` +
      `role="progressbar" style="width: ${result.pct}%;" aria-valuenow="${fg}" aria-valuemin="${data.fg.low}" ` +
      `aria-valuemax="${data.fg.high}">${fg}</div></div>`);
  } else {
    $('#estimated-fg').text(fg);
  }
}

// Calculate ABV
function calculate_abv() {
  return (calculateOG() - calculateFG()) * 131.25;
}

// Display ABV
function displayABV(data) {
  var abv = calculate_abv().toFixed(1);
  if (data !== null) {
    var result = calculatePct(abv, data.abv.low, data.abv.high)
    $('#estimated-abv').html(`<div class="progress spec-progress"><div class="progress-bar ${result.color}" ` +
      `role="progressbar" style="width: ${result.pct}%;" aria-valuenow="${abv}" aria-valuemin="${data.abv.low}" ` +
      `aria-valuemax="${data.abv.high}">${abv} %/vol.</div></div>`);
  } else {
    $('#estimated-abv').text(`${abv} %/vol.`);
  }
}

// Calculate IBU
function calculateIBU() {
  var hopsLength = $('#hops').data('length');
  if (hopsLength == 0) {
    return 0;
  }

  var bigness = 1.65 * Math.pow(0.000125, calculateOG() - 1);
  var ibu = 0;
  var volume = parseFloat($(`#volume`).val()) || 0;
  for (var i = 0; i < hopsLength; i++) {
    var use = $(`#hops-${i}-use`).val();
    if (use != 'Boil' && use != 'FWH') {
      continue;
    }
    var alpha = parseFloat($(`#hops-${i}-alpha`).val()) || 0.0;
    var amt = parseFloat($(`#hops-${i}-amount`).val()) || 0.0;
    var duration = parseFloat($(`#hops-${i}-duration`).val()) || 0.0;
    var mgl = alpha * amt * 7490 / (volume * 100)
    var btf = (1 - Math.pow(Math.E, -0.04 * duration)) / 4.15
    ibu += bigness * btf * mgl;
  }
  return ibu;
}

// Display IBU
function displayIBU(data) {
  var ibu = calculateIBU().toFixed();

  if (data !== null) {
    var result = calculatePct(ibu, data.ibu.low, data.ibu.high)
    $('#estimated-ibu').html(`<div class="progress spec-progress"><div class="progress-bar ${result.color}" ` +
      `role="progressbar" style="width: ${result.pct}%;" aria-valuenow="${ibu}" aria-valuemin="${data.ibu.low}" ` +
      `aria-valuemax="${data.ibu.high}">${ibu} IBU</div></div>`);
  } else {
    $('#estimated-ibu').text(`${ibu} IBU`);
  }
}

// Calculate IBU Ratio
function calculateIBURatio() {
  return 0.001 * calculateIBU() / (calculateOG() - 1)
}

// Display IBU Ratio
function displayIBURatio() {
  var iburatio = calculateIBURatio().toFixed(3);
  $('#estimated-iburatio').text(`${iburatio} IBU/OG`);
}

// Calculate SRM
function calculateSRM() {
  var fermsLength = $('#ferms').data('length');
  if (fermsLength == 0) {
    return 0;
  }
  var mcu = 0;
  var volume = parseFloat($(`#volume`).val()) || 0;
  for (var i = 0; i < fermsLength; i++) {
    var color = parseFloat($(`#fermentables-${i}-color`).val()) || 0.0;
    var amt = parseFloat($(`#fermentables-${i}-amount`).val()) || 0.0;
    mcu += amt * color / volume;
  }
  return 1.4922 * Math.pow(mcu, 0.6859)
}

// Display SRM
function displaySRM(data) {
  var srm = calculateSRM().toFixed();
  if (data !== null) {
    var result = calculatePct(srm, data.srm.low, data.srm.high)
    $('#estimated-srm').html(`<div class="progress spec-progress"><div class="progress-bar ${result.color}" ` +
      `role="progressbar" style="width: ${result.pct}%;" aria-valuenow="${srm}" aria-valuemin="${data.srm.low}" ` +
      `aria-valuemax="${data.srm.high}">${srm} SRM</div></div>`);
  } else {
    $('#estimated-srm').text(`${srm} SRM`);
  }
}

// Display all specifications
function displayAll() {
  $.getJSON(getSpecsURL()).done(
    function (json) {
      displayOG(json);
      displayFG(json);
      displayABV(json);
      displayIBU(json);
      displayIBURatio();
      displaySRM(json);
    }
  ).fail(
    function () {
      displayOG(null);
      displayFG(null);
      displayABV(null);
      displayIBU(null);
      displayIBURatio();
      displaySRM(null);
    }
  );
}

$(document).ready(function() {
  // Register clicks
  $('#add-ferm').click(addFerm);
  $('.rem-ferm').click(removeFerm);
  $('#add-hop').click(addHop);
  $('.rem-hop').click(removeHop);
  $('#add-step').click(addMashStep);
  $('.rem-step').click(removeMashStep);

  // Register change events
  rebindChangeEvents();

  // Update specifications
  displayAll();
});
