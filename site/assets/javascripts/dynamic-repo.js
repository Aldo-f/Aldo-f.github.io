(function() {
  'use strict';
  
  var path = window.location.pathname;
  var map = {"thuis/": {"url": "https://github.com/Aldo-f/thuis", "name": "Aldo-f/thuis"}, "thuis-v3/": {"url": "https://github.com/Aldo-f/thuis", "name": "Aldo-f/thuis"}, "thuis-v4/": {"url": "https://github.com/Aldo-f/thuis", "name": "Aldo-f/thuis"}, "thuis-v5/": {"url": "https://github.com/Aldo-f/thuis", "name": "Aldo-f/thuis"}, "clock/": {"url": "https://github.com/Aldo-f/clock", "name": "Aldo-f/clock"}, "blanky/": {"url": "https://gitlab.com/Aldo-f/blanky", "name": "Aldo-f/blanky"}, "blanky-v1/": {"url": "https://gitlab.com/Aldo-f/blanky", "name": "Aldo-f/blanky"}, "opencode-multi-model-fallback/": {"url": "https://github.com/Aldo-f/opencode-multi-model-fallback", "name": "Aldo-f/opencode-multi-model-fallback"}};
  var defaultUrl = "https://github.com/Aldo-f/Aldo-f.github.io";
  var defaultName = "Aldo-f/Aldo-f.github.io";
  var repoUrl = defaultUrl;
  var repoName = defaultName;
  
  for (var prefix in map) {
    if (path.indexOf(prefix) === 0 || path.indexOf('/' + prefix) !== -1) {
      repoUrl = map[prefix].url;
      repoName = map[prefix].name;
      break;
    }
  }
  
  function updateRepoSource() {
    var sources = document.querySelectorAll('[data-md-component="source"]');
    sources.forEach(function(source) {
      // The source element IS the <a> tag, not a container
      var link = source;
      var repoDiv = source.querySelector('.md-source__repository');
      if (link) link.href = repoUrl;
      if (repoDiv) {
        repoDiv.textContent = repoName;
        // Fetch and append stats
        fetchRepoStats(repoUrl, repoDiv);
      }
    });
  }
  
  function fetchRepoStats(url, element) {
    var api_url;
    var is_gitlab = url.includes('gitlab.com');
    var is_github = url.includes('github.com');
    
    if (is_github) {
      var match = url.match(/github\.com\/(.+)\/(.+)/);
      if (match) {
        api_url = 'https://api.github.com/repos/' + match[1] + '/' + match[2];
        fetch(api_url)
          .then(function(r) { return r.json(); })
          .then(function(data) {
            var stats = [];
            if (data.stargazers_count) stats.push('⭐ ' + formatNumber(data.stargazers_count));
            if (data.forks_count) stats.push('🍴 ' + formatNumber(data.forks_count));
            if (stats.length > 0) {
              element.innerHTML = repoName + ' <span class="repo-stats">' + stats.join(' ') + '</span>';
            }
          })
          .catch(function() {});
      }
    } else if (is_gitlab) {
      var match = url.match(/gitlab\.com\/(.+)\/(.+)/);
      if (match) {
        api_url = 'https://gitlab.com/api/v4/projects/' + match[1] + '%2F' + match[2];
        fetch(api_url)
          .then(function(r) { return r.json(); })
          .then(function(data) {
            var stats = [];
            if (data.star_count) stats.push('⭐ ' + formatNumber(data.star_count));
            if (data.forks_count) stats.push('🍴 ' + formatNumber(data.forks_count));
            if (stats.length > 0) {
              element.innerHTML = repoName + ' <span class="repo-stats">' + stats.join(' ') + '</span>';
            }
          })
          .catch(function() {});
      }
    }
  }
  
  function formatNumber(n) {
    if (n >= 1000) {
      return (n / 1000).toFixed(1) + 'k';
    }
    return n.toString();
  }
  
  // Run on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', updateRepoSource);
  
  // Also run on instant loading (pjax) - Material theme fires 'md-navigator-ready' or similar
  document.addEventListener('pjax:complete', updateRepoSource);
  document.addEventListener('md-content-loaded', updateRepoSource);
  
  // And also run on any navigation (popstate for history API)
  window.addEventListener('popstate', updateRepoSource);
  
  // Run immediately in case DOM is already ready
  if (document.readyState !== 'loading') {
    updateRepoSource();
  }
})();
