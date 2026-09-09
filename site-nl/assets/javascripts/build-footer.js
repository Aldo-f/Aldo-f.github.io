(function () {
  'use strict';
  var raw = typeof BUILD_TIME !== 'undefined' ? BUILD_TIME : null;
  if (!raw) return;
  var d = new Date(raw);
  var formatted = d.getFullYear() + '-' +
    String(d.getMonth()+1).padStart(2,'0') + '-' +
    String(d.getDate()).padStart(2,'0') + ' ' +
    String(d.getHours()).padStart(2,'0') + ':' +
    String(d.getMinutes()).padStart(2,'0') + ' ' +
    d.toLocaleTimeString(undefined, {timeZoneName:'short'});
  var el = document.getElementById('build-timestamp');
  if (el) el.textContent = '— Build ' + formatted;
})();
