function buttons(e, app_id){
      var btn_accept = document.getElementById('accept' + app_id);
      if (e.target.checked){
        btn_accept.removeAttribute('disabled');
       }
      else{
       btn_accept.setAttribute('disabled', 'disabled');
       }
  }
