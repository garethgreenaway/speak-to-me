$('form :submit.ajax_single_submit').live('click', function(e) {
  e.preventDefault();

  // Get the form for the submit button being pressed
  var form = $('#' + this.id).parents('form').get(0).id
  console.log(form)
  
  // Serial the data and send it along to the send_form function
  data = $('#' + form).serializeObject();
  Dajaxice.home.send_form(Dajax.process, {'form':data,'form_id':form});
});

$('form :submit.ajax_submit').live('click', function(e) {
  e.preventDefault();

  // Get the form for the submit button being pressed
  var form = $('#' + this.id).parents('form').get(0).id
  console.log(form)
  
  // Serial the data and send it along to the send_form function
  data = $('#' + form).serializeObject();
  Dajaxice.home.send_form(Dajax.process, {'form':data,'form_id':form});
});

$('form :submit.ajax_skip').live('click', function(e) {
  e.preventDefault();

  // Get the form for the submit button being pressed
  var form = $('#' + this.id).parents('form').get(0).id
  console.log(form)

  switchTab();  

});

function js_callback(data) {
  
  if (data.result == 'success') {
    lockForm(data.form_id)
    switchTab()
  }
}

function lockForm(form_id) {

  var form = document.forms[form_id];
  
  for(i=0; i < form.elements.length; i++) {
    classes = form.elements[i].getAttribute("class");
    classes = classes + " disabled"
    form.elements[i].setAttribute("class", classes);
    form.elements[i].setAttribute("disabled", "true")
  }
  
}

function switchTab(){
      
  if(isLastTab()) 
    /* alert('submitting the form...'); */
    /* Navigate back to the main page */
    window.location.href = "/"
  else 
    nextTab();

  $('a[data-toggle="tab"]').on('shown', function (e) {
    isLastTab();
  });
}

function nextTab() {
  var e = $('#myTab li.active').next().find('a[data-toggle="tab"]');
  if(e.length > 0) e.click();  
  isLastTab();
}

function isLastTab() {
  var e = $('#myTab li:last').hasClass('active'); 
  return e;
}
