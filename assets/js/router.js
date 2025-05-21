// get JSON data from file & return to caller
async function getJSONData(file) {
  let data = await fetch(file);
  return await data.json();
}

const locationHandler = async () => {

  let routes = await getJSONData("./assets/js/sitemap.json");
  // get the url path, replace hash with empty string
  var location = window.location.hash.replace("#", "");
  // if the path length is 0, set it to primary page route
  if (location.length == 0) {
    location = "/";
  }

  let k = null;
  let v = null;
  let breakCheck = false;

  for (key in routes) {
    if (breakCheck) {
      break;
    }
    k = key;
    for (val in routes[key]) {
      if (val == location) {
        v = routes[key];
        breakCheck = true;
        break;
      }
    }
  }

  console.log(k);
  console.log(v);
  let r = "";

  for (e in v) {
    console.log(v[e].message);


    href = v[e].title.toLowerCase();
    href = href.replaceAll(" ", "");
    console.log(href);

    r += "<a href=\"#" + href + "\">" + v[e].title + "</a>";
  }

  //<!-- <a href="#page1">Page 1</a> -->

  // get the route object from the routes object
  const route = routes[k][location] || routes["404"];
  // get the html from the template
  const html = await fetch(route.template).then((response) => response.text());
  // set the content of the content div to the html
  document.getElementById("content").innerHTML = html;

  if (location != "/" && location != "404") {
    document.getElementById("sidebarLinks").innerHTML = r;
  }
  // set the title of the document to the title of the route
  document.title = route.title;

  //document.getElementById("message").innerText = route.message;
};

// create a function that watches the hash and calls the urlLocationHandler
window.addEventListener("hashchange", locationHandler);
// call the urlLocationHandler to load the page
locationHandler();