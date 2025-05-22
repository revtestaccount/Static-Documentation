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

  // create html that will be inserted into the 'sidebarLinks' element on our page
  let sidebarLinksToRender = "";

  for (aRoute in routeValue) {
    href = routeValue[aRoute].title.toLowerCase();
    href = href.replaceAll(" ", "");

    if (href != 'home' && href != '404pagenotfound') {
      sidebarLinksToRender += "<a href=\"#" + href + "\">" + routeValue[aRoute].title + "</a>";
    }
  }

  // get the route object from the routes object
  const route = jsonData[routeKey][location] || jsonData['home']["404"];
  // get the html from the template
  const html = await fetch(route.template).then((response) => response.text());
  // set the content of the content div to the html
  document.getElementById("content").innerHTML = html;

  document.getElementById("sidebarLinks").innerHTML = sidebarLinksToRender;
  // set the title of the document to the title of the route
  document.title = route.title;

  //document.getElementById("message").innerText = route.message;
};

// create a function that watches the hash and calls the urlLocationHandler
window.addEventListener("hashchange", locationHandler);
// call the urlLocationHandler to load the page
locationHandler();