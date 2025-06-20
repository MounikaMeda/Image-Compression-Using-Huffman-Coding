function uploadImage() {
  const input = document.getElementById('imageInput');
  const file = input.files[0];
  const formData = new FormData();
  formData.append('image', file);

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('result').innerHTML = `
      <p>Original Size: ${data.originalSize} bytes</p>
      <p>Compressed Size: ${data.compressedSize} bytes</p>
      <p>Compression Ratio: ${data.ratio}</p>
      <p><a href="/${data.compressedFile}" download>Download Compressed File</a></p>
    `;
  })
  .catch(err => console.error('Upload failed', err));
}
