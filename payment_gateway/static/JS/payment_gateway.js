var index = 0;

autoSlide();
function autoSlide(){
  var i;
  var slides = document.getElementsByClassName("mySlides");

  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  index++;

  if (index > slides.length) { index = 1 }

  slides[index-1].style.display = "block";
  setTimeout(autoSlide, 5000);
}

function confirmDelete(){
  return confirm('Do you want to remove this item from cart?');
}
