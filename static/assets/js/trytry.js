( function ( $ ) {
    "use strict";

var ctx = $('#Zhongguancun');

const brandPrimary = '#20a8d8'
const brandSuccess = '#4dbd74'
const brandInfo = '#63c2de'
const brandDanger = '#f86c6b'
const brandyellow = '#FFF700'
const brandblack = '#000000'

function convertHex (hex, opacity) {
  hex = hex.replace('#', '')
  const r = parseInt(hex.substring(0, 2), 16)
  const g = parseInt(hex.substring(2, 4), 16)
  const b = parseInt(hex.substring(4, 6), 16)

  const result = 'rgba(' + r + ',' + g + ',' + b + ',' + opacity / 100 + ')'
  return result
}

    const timePeriod = $("#nav-home-tab-week").attr('timeperiod');
    console.log(timePeriod)
      fetch('/api?timeperiod=' + timePeriod)
      .then(function(response) {
        return response.json();
      }).then(function(Data) {

    jQuery.getScript("assets/js/same.js")

    })
})
( jQuery );