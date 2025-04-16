let idCounter = 0;

function saveData() {
  // Get form data 
  const name = document.getElementById('name').value;

  // Create a Blob from the data 
  const blob = new Blob([name], { type: 'text/plain' });

  // Create a link element 
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'editor_output.txt'; // File name

  // Append link to the body (not visible) 
  document.body.appendChild(link);

  // Programmatically click the link to trigger download 
  link.click();

  // Clean up and remove the link 
  document.body.removeChild(link);
}

function spawnTextBox() {
  let tb = document.createElement('textarea');
  tb.className = "form-control";
  tb.id = idCounter;
  tb.rows = 10;
  document.getElementById("form").insertBefore(tb, document.getElementById("savebutton"));
  idCounter++;
}

function spawnTitle() {
  let title = document.createElement('textarea');
  title.className = "form-control";
  title.id = idCounter;
  title.rows = 1;
  document.getElementById("form").insertBefore(title, document.getElementById("savebutton"));
  idCounter++;
}

