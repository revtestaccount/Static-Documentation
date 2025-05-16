const routes = {
  "/": {
    template: "/templates/home.html",
    title: "Home",
    message: "This is the home page",
  },
  page1: {
    template: "/templates/page1.html",
    title: "Page 1",
    message: "placeholder text/unused",
  },
  page2: {
    template: "/templates/page2.html",
    title: "Page 2",
    message: "placeholder text/unused",
  },
  page3: {
    template: "/templates/page3.html",
    title: "Page 3",
    message: "placeholder text/unused",
  },
  pitselfserviceguide: {
    template: "/templates/pitselfserviceguide.html",
    title: "PIT Self Service Application Guide",
    message: "placeholder text/unused",
  },
  toctest: {
    template: "/templates/toctest.html",
    title: "Table of contents test 1",
    message: "placeholder text/unused",
  },
  toctest2: {
    template: "/templates/toctest2.html",
    title: "Table of contents test 2",
    message: "placeholder text/unused",
  }
};

const locationHandler = async () => {
  // get the url path, replace hash with empty string
  var location = window.location.hash.replace("#", "");
  // if the path length is 0, set it to primary page route
  if (location.length == 0) {
    location = "/";
  }

  // get the route object from the routes object
  const route = routes[location];
  // get the html from the template
  const html = await fetch(route.template).then((response) => response.text());
  // set the content of the content div to the html
  document.getElementById("content").innerHTML = html;
  // set the title of the document to the title of the route
  document.title = route.title;

  //document.getElementById("message").innerText = route.message;
};

// create a function that watches the hash and calls the urlLocationHandler
window.addEventListener("hashchange", locationHandler);
// call the urlLocationHandler to load the page
locationHandler();