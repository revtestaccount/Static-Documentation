
const app = document.getElementById('app');

const routes = {
  home: 'home.html',
  soap: 'soap.html',
  rest: 'rest.html',
  signature: 'signature.html',
  newpage: 'newpage.html',
  PITSelfServiceGuide: 'PITSelfServiceGuide.html',
};

function loadRoute() {
  const hash = window.location.hash.slice(1) || 'home';
  const route = routes[hash] || 'home.html';

  fetch(route)
    .then(res => res.text())
    .then(html => {
      app.innerHTML = html;
    })
    .catch(() => {
      app.innerHTML = '<h2>Page not found.</h2>';
    });
}

window.addEventListener('hashchange', loadRoute);
window.addEventListener('load', loadRoute);
