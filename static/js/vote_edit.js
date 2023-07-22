function add_variant() {
    'use_strict'
    let fields_count = Number(count.innerHTML)
    let xhr = new XMLHttpRequest();
    xhr.open('get', '/voting/'+ voting_identifier.value + '/variants/create/')
    xhr.send()
    xhr.onload = function() {
      html = xhr.response
      variants_container.insertAdjacentHTML('beforeEnd', html);
      count.innerHTML = String(fields_count+1)
    };
    xhr.onerror = function() { // происходит, только когда запрос совсем не получилось выполнить
      alert(`Ошибка соединения`);
    };
}
