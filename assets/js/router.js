
const app = document.getElementById('app');


function getData() {
  return fetch('./assets/js/sitemap.json')
    .then(response => response.json())
    .then(data => {
      return data
    })
};

(async () => {
  const routes = await getData()
  //console.log(data)

  function loadRoute() {
    const hash = window.location.hash.slice(1);
    const route = routes[hash];

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

})()




