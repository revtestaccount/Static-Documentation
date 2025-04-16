let idCounter = 0;

function saveData() {

  /* */
  var queryAll = document.querySelectorAll("*")

  let x = Array.from(queryAll)

  let alldata = "";

  x.forEach((element) => {
    //console.log(element.value);

    if(element.id == 'paragraph'){
      alldata += element.value + "\n";
    }

    if(element.id == 'title'){
      alldata += "# " + element.value + "\n";
    }

    if(element.id == 'heading'){
      alldata += "## " + element.value + "\n";
    }

});

console.log(x)

 
  

  /* */

  // Get form data 
  //const name = document.getElementById('0').value;

  // Create a Blob from the data 
  //const blob = new Blob([name], { type: 'text/plain' });
  const blob = new Blob([alldata], { type: 'text/plain' });

  // Create a link element 
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'editor_output.md'; // File name

  // Append link to the body (not visible) 
  document.body.appendChild(link);

  // Programmatically click the link to trigger download 
  link.click();

  // Clean up and remove the link 
  document.body.removeChild(link);
}

function spawnTextBox() {
  let label = document.createElement('p');
  label.textContent = "Paragraph:"

  let tb = document.createElement('textarea');
  tb.className = "form-control";
  tb.id = "paragraph";
  tb.rows = 10;
  document.getElementById("form").insertBefore(label, document.getElementById("savebutton"));
  document.getElementById("form").insertBefore(tb, document.getElementById("savebutton"));
  idCounter++;
}

function spawnTitle() {
  let label = document.createElement('p');
  label.textContent = "Document title:"

  let title = document.createElement('textarea');
  title.className = "form-control";
  title.id = "title";
  title.rows = 1;
  document.getElementById("form").insertBefore(label, document.getElementById("savebutton"));
  document.getElementById("form").insertBefore(title, document.getElementById("savebutton"));
  idCounter++;
}

function spawnHeading() {
  let label = document.createElement('p');
  label.textContent = "Heading::"

  let title = document.createElement('textarea');
  title.className = "form-control";
  title.id = "heading";
  title.rows = 1;
  document.getElementById("form").insertBefore(label, document.getElementById("savebutton"));
  document.getElementById("form").insertBefore(title, document.getElementById("savebutton"));
  idCounter++;
}

