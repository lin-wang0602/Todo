//api call
const categorySelect = document.getElementById('category');
// store the url of selected image
const imageUrlInput = document.querySelector('input[name="image_url"]');
//display the image
const imagePreview = document.getElementById('image-preview');

categorySelect.addEventListener('change', () => {
  const category = categorySelect.value;
  const url = `/api/pexels/${category}`;
  // makes a fetch call to url returns a promise and then response converted to JSON
      fetch(url)
        .then(response => response.json())
        .then(data => {
          const photos = data.photos
          //get the random photo
          const randomIndex = Math.floor(Math.random() * photos.length)
          const imageUrl = photos[randomIndex].src.medium;
          imagePreview.src = imageUrl; // set its attrobute to the url of the selected image
          imagePreview.style.display = 'block';
          imageUrlInput.value = imageUrl;
        });
    });
