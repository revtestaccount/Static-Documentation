function saveData() { 
  // Get form data 
const name = document.getElementById('name').value; 

  // Create a Blob from the data 
  const blob = new Blob([name], { type: 'text/plain' }); 

  // Create a link element 
  const link = document.createElement('a'); 
  link.href = URL.createObjectURL(blob); 
  link.download = 'formData.txt'; // File name 

  // Append link to the body (not visible) 
  document.body.appendChild(link); 
   
  // Programmatically click the link to trigger download 
  link.click(); 
   
  // Clean up and remove the link 
  document.body.removeChild(link); 
} 