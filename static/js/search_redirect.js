function redirect(){
  let a = search.value;
  window.location.replace(search_url.value + '?title=' + a);
}

document.getElementById('search').onkeypress = function($) {
  if ($.keyCode === 13) {
    redirect();
  }
}
