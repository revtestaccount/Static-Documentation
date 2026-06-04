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
  for (key in jsonData) {
    if (breakCheck) {
      break;
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

  // create html that will be inserted into the 'navLinksList' element on our page
  let sidebarLinksToRender = "";

  // On the home page use the dedicated home_nav group for nav links
  const navSource = (location === "/") ? jsonData["home_nav"] : routeValue;

  /* Code relating to the following:
   'soapschemareferencecurrentversion'
   'soapschemareferencenextversion'
   'restapireferencecurrentversion'
   'restapireferencenextversion'
   is hard coded and for demonstration purposes only.
   Needs to be reworked. */


  for (aRoute in navSource) {
    href = navSource[aRoute].title.toLowerCase();
    href = href.replaceAll(" ", "");

    if (href != 'home' && href != '404pagenotfound' && href != 'soapschemareferencecurrentversion' && href != 'soapschemareferencenextversion' && href != 'restapireferencecurrentversion' && href != 'restapireferencenextversion') {
      sidebarLinksToRender += "<li class=\"nav-item\"><a class=\"nav-link site-nav__link\" href=\"#" + aRoute + "\">" + navSource[aRoute].title + "</a></li>";
    }

    if (href == "soapschemareferencecurrentversion") {
      sidebarLinksToRender += "<li class=\"nav-item\"><a class=\"nav-link site-nav__link\" href=\"./templates/schemas/PIT3/soap/soap-schema-reference/webframe.html\" target=\"_blank\" rel=\"noopener noreferrer\">SOAP Schema Reference Current Version</a></li>";
    }

    if (href == "soapschemareferencenextversion") {
      sidebarLinksToRender += "<li class=\"nav-item\"><a class=\"nav-link site-nav__link\" href=\"./templates/schemas/PIT4/soap/soap-schema-reference/webframe.html\" target=\"_blank\" rel=\"noopener noreferrer\">SOAP Schema Reference Next Version</a></li>";
    }

    if (href == "restapireferencecurrentversion") {
      sidebarLinksToRender += "<li class=\"nav-item\"><a class=\"nav-link site-nav__link\" href=\"./templates/schemas/PIT3/rest/paye-employers-rest-api-pit3.html\" target=\"_blank\" rel=\"noopener noreferrer\">REST API Reference Current Version</a></li>";
    }

    if (href == "restapireferencenextversion") {
      sidebarLinksToRender += "<li class=\"nav-item\"><a class=\"nav-link site-nav__link\" href=\"./templates/schemas/PIT4/rest/paye-employers-rest-api-pit4.html\" target=\"_blank\" rel=\"noopener noreferrer\">REST API Reference Next Version</a></li>";
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