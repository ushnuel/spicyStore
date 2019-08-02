
const openDrawer = () => {
  const eve = document.getElementsByClassName('sideDrawer');
  const state = eve[0].style.display;
  if (state === 'block') {
    eve[0].style.display = "none";
    return
  }
  eve[0].style.display = "block";
}

$(window).on("load", function () {
  console.log('I reached here')
  $('#preload').delay(4000).fadeOut('slow', function () {
    $(this).remove();
  });
});