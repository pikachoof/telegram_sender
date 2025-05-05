var apiId;
var apiHash;

function handleFileUpload() {
    const fileUploadInput = document.getElementById('fileUploadInput');
    fileUploadInput.click();
}

function uploadFile() {
    const fileInput = document.getElementById('fileUploadInput');
    const fileNameDisplay = document.getElementById('fileNameDisplay');

    // Can choose only 1 file for the API Key
    const file = fileInput.files[0];
    fileNameDisplay.textContent = file.name;

    //extractCredentials(file.textContent, apiId, apiHash);
    //alert(apiId, apiHash);
}

document.getElementById('fileUploadInput').addEventListener('change', uploadFile);

document.addEventListener('DOMContentLoaded', () => {
  const sendButton = document.getElementById('saveButton');
  const messageInput = document.getElementById('messageInput');

  sendButton.addEventListener('click', async () => {
      const textToSend = messageInput.value;
      if (textToSend.trim() !== '') {
          try {
              const response = await fetch('http://localhost:5000/send_to_saved', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({ text: textToSend }),
              });

              const data = await response.json();
              if (data.status === 'success') {
                  alert('Message sent to Saved Messages!');
                  messageInput.value = '';
              } else {
                  alert(`Error sending message: ${data.error || 'Unknown error'}`);
              }
          } catch (error) {
              alert(`Network error: ${error.message}`);
          }
      } else {
          alert('Please enter some text.');
      }
  });
});