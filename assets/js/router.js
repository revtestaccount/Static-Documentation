// get JSON data from file & return to caller
async function getJSONData(file) {
  let data = await fetch(file);
  return await data.json();
}

const locationHandler = async () => {

  let jsonData = await getJSONData("./assets/js/sitemap.json");
  // get the url path, replace hash with empty string
  var location = window.location.hash.replace("#", "");
  // if the path length is 0, set it to primary page route
  if (location.length == 0) {
    location = "/";
  }

  let routeKey = "";
  let routeValue = "";
  let breakCheck = false;

  //find the block of json that contains the route information we need
  // Skip home_nav — it is only used for nav rendering, not content lookup
  for (key in jsonData) {
    if (breakCheck) {
      break;
    }
    if (key === "home_nav" || key === "nav_groups") {
      continue;
    }
    routeKey = key;
    for (val in jsonData[key]) {
      if (val == location) {
        routeValue = jsonData[key];
        breakCheck = true;
        break;
      }
    }
  }

  // ── Build nav links ─────────────────────────────────────────────────────────
  let sidebarLinksToRender = "";

  const navGroups = jsonData["nav_groups"];
  const homeNav   = jsonData["home_nav"];

  // Helper: find all route titles/templates across all route groups by key
  function findRoute(key) {
    for (let group in jsonData) {
      if (group === "home_nav" || group === "nav_groups") continue;
      if (jsonData[group][key]) return jsonData[group][key];
    }
    return null;
  }

  // Helper: find which nav_group parent a given route key belongs to
  function findParentGroup(key) {
    for (let groupKey in navGroups) {
      if (groupKey === key) return groupKey;                    // is itself a parent
      if (navGroups[groupKey].children.includes(key)) return groupKey;
    }
    return null;
  }

  if (location === "/") {
    // ── Home page: flat links for all 6 cards ──────────────────────────────
    for (let key in homeNav) {
      sidebarLinksToRender += `<li class="nav-item"><a class="nav-link site-nav__link" href="#${key}">${homeNav[key].title}</a></li>`;
    }

  } else {
    // ── Inner pages: find parent group and render dropdown ─────────────────
    const parentKey = findParentGroup(location);

    if (parentKey && navGroups[parentKey]) {
      const group    = navGroups[parentKey];
      const children = group.children;
      const isOnCardPage = (location === parentKey);

      // Dropdown toggle — label is the parent card title
      sidebarLinksToRender += `
        <li class="nav-item dropdown">
          <a class="nav-link site-nav__link site-nav__dropdown-toggle dropdown-toggle"
             href="#${parentKey}"
             role="button"
             data-bs-toggle="dropdown"
             aria-expanded="false">
            ${group.label}
          </a>
          <ul class="dropdown-menu site-nav__dropdown-menu">`;

      // Parent card page link at top of dropdown
      sidebarLinksToRender += `
            <li>
              <a class="dropdown-item site-nav__dropdown-item${isOnCardPage ? ' active' : ''}" href="#${parentKey}">
                Overview
              </a>
            </li>
            <li><hr class="dropdown-divider site-nav__divider"></li>`;

      // Child pages
      for (let childKey of children) {
        const childRoute = findRoute(childKey);
        if (!childRoute) continue;

        const isActive  = (location === childKey);
        const childTitle = childRoute.title;

        // Handle hard-coded external links
        if (childKey === "soapschemareferencecurrentversion") {
          sidebarLinksToRender += `<li><a class="dropdown-item site-nav__dropdown-item" href="./templates/schemas/PIT3/soap/soap-schema-reference/webframe.html" target="_blank" rel="noopener noreferrer">${childTitle}</a></li>`;
        } else if (childKey === "soapschemareferencenextversion") {
          sidebarLinksToRender += `<li><a class="dropdown-item site-nav__dropdown-item" href="./templates/schemas/PIT4/soap/soap-schema-reference/webframe.html" target="_blank" rel="noopener noreferrer">${childTitle}</a></li>`;
        } else if (childKey === "restapireferencecurrentversion") {
          sidebarLinksToRender += `<li><a class="dropdown-item site-nav__dropdown-item" href="./templates/schemas/PIT3/rest/paye-employers-rest-api-pit3.html" target="_blank" rel="noopener noreferrer">${childTitle}</a></li>`;
        } else if (childKey === "restapireferencenextversion") {
          sidebarLinksToRender += `<li><a class="dropdown-item site-nav__dropdown-item" href="./templates/schemas/PIT4/rest/paye-employers-rest-api-pit4.html" target="_blank" rel="noopener noreferrer">${childTitle}</a></li>`;
        } else {
          sidebarLinksToRender += `<li><a class="dropdown-item site-nav__dropdown-item${isActive ? ' active' : ''}" href="#${childKey}">${childTitle}</a></li>`;
        }
      }

      sidebarLinksToRender += `
          </ul>
        </li>`;
    }
  }

  // get the route object from the routes object
  const route = jsonData[routeKey][location] || jsonData['home']["404"];
  // get the html from the template
  const html = await fetch(route.template).then((response) => response.text());
  // set the content of the content div to the html
  document.getElementById("content").innerHTML = html;

  document.getElementById("navLinksList").innerHTML = sidebarLinksToRender;
  // set the title of the document to the title of the route
  document.title = route.title;

  //document.getElementById("message").innerText = route.message;
};

// create a function that watches the hash and calls the urlLocationHandler
window.addEventListener("hashchange", locationHandler);
// call the urlLocationHandler to load the page
locationHandler();