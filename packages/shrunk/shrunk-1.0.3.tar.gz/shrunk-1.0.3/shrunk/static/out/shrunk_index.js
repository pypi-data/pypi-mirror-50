var shrunk=shrunk||function(){}
var clear_search=function(){var url=new URL(window.location.href);var sortBy=url.searchParams.get("sortby");var all_users=url.searchParams.get("all_users");if(sortBy===null){sortBy="0"}
if(all_users===null){all_users=1;}
window.location.replace("/?all_users="+all_users+"&search=&sortby="+sortBy);}
function toggleLinks(cb,netid){$("article.link-group").each(function(){if(cb.checked)
$(this).css("display","block");else{link_info=$(this).children(".link-info");if($(link_info).children(".owner").attr("netid")!=netid)
$(this).css("display","none");}});}
const CSRF_TOKEN=$('meta[name=csrf-token]').attr('content');$.ajaxSetup({beforeSend:function(xhr,settings){xhr.setRequestHeader('X-CSRFToken',CSRF_TOKEN);}});const ADD_LINK_FORM={'endpoint':'/add','field_element_prefix':'#add-link-','fields':['title','long_url','short_url'],'fields_clear':['title','long_url','short_url']};const EDIT_LINK_FORM={'endpoint':'/edit','field_element_prefix':'#edit-link-','fields':['title','long_url','short_url','old_short_url'],'fields_clear':['title','long_url','short_url']};function copy_short_url(ev){var parent=ev.target.parentElement;if(parent.tagName=='BUTTON')
parent=parent.parentElement;const link=parent.querySelector('.short-url');var text_area=document.createElement('textarea');text_area.value=link.href;document.body.appendChild(text_area);text_area.select();document.execCommand('Copy');text_area.remove();}
function delete_link(ev){var parent=ev.target.parentElement;if(parent.tagName=='BUTTON')
parent=parent.parentElement;const link_id=parent.querySelector('.link-id').value;$('#link-delete-id').val(link_id);$('#link-delete-modal').modal();}
function do_delete_link(){const link_id=$('#link-delete-id').val();$('#link-delete-id').val();const req={'short_url':link_id};$.post('/delete',req,function(){location.reload();});}
function edit_link(ev){var parent=ev.target.parentElement;if(parent.tagName=='BUTTON')
parent=parent.parentElement;const link_id=parent.querySelector('.link-id').value;const title=parent.querySelector('.link-title').value;const long_url=parent.querySelector('.link-url').value;$('#link-edit-modal-title').html('Editing <em>'+link_id+'</em>');$('#edit-link-old_short_url').val(link_id);$('#edit-link-title').val(title);$('#edit-link-long_url').val(long_url);$('#edit-link-short_url').val(link_id);$('#link-edit-modal').modal();}
function change_sortby(sortby){window.location.replace('/?sortby='+sortby);}
function change_links_set(new_set){window.location.replace('/?links_set='+new_set);}
function clear_form(form){const prefix=form['field_element_prefix'];form['fields_clear'].forEach(function(field,index){$(prefix+field).val('');$(prefix+field).removeClass('is-invalid');$(prefix+field+'-feedback').hide('is-invalid');});}
function send_request_keypress(ev,form){if(ev.keyCode==13){ev.preventDefault();send_request(form);}}
function send_request(form){const prefix=form['field_element_prefix'];var req={};form['fields'].forEach(function(field,index){if($(prefix+field).length){req[field]=$(prefix+field).val();}});$.ajax({type:'POST',url:form['endpoint'],data:req,error:(jqXHR,textStatus,errorThrown)=>process_errors(form,jqXHR.responseJSON['errors']),success:resp=>process_success(form,resp['success']),dataType:'json'});}
function process_errors(form,errors){const prefix=form['field_element_prefix'];form['fields'].forEach(function(field,index){if(errors.hasOwnProperty(field)){$(prefix+field).addClass('is-invalid');$(prefix+field+'-feedback').html(errors[field]);$(prefix+field+'-feedback').show();}else{$(prefix+field).removeClass('is-invalid');$(prefix+field+'-feedback').hide();}});}
function process_success(form,resp){location.reload();}