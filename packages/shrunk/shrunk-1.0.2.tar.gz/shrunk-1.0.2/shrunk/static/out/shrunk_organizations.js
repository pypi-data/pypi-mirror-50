var shrunk=shrunk||function(){}
var clear_search=function(){var url=new URL(window.location.href);var sortBy=url.searchParams.get("sortby");var all_users=url.searchParams.get("all_users");if(sortBy===null){sortBy="0"}
if(all_users===null){all_users=1;}
window.location.replace("/?all_users="+all_users+"&search=&sortby="+sortBy);}
function toggleLinks(cb,netid){$("article.link-group").each(function(){if(cb.checked)
$(this).css("display","block");else{link_info=$(this).children(".link-info");if($(link_info).children(".owner").attr("netid")!=netid)
$(this).css("display","none");}});}
const CSRF_TOKEN=$('meta[name=csrf-token]').attr('content');$.ajaxSetup({beforeSend:function(xhr,settings){xhr.setRequestHeader('X-CSRFToken',CSRF_TOKEN);}});const CREATE_ORG_FORM={'endpoint':'/orgs/create','field_element_prefix':'#create-org-','fields':['name'],'fields_clear':['name']};var org_delete_name;var org_delete_fn;function delete_org_list(ev){var parent=ev.target.parentElement;if(parent.tagName=='BUTTON')
parent=parent.parentElement;org_delete_name=parent.querySelector('.org-name').value;org_delete_fn=function(){location.reload();};$('#org-delete-modal').modal();}
function delete_org_manage(name){org_delete_name=name;org_delete_fn=function(){window.location.replace('/orgs');};$('#org-delete-modal').modal();}
function do_delete_org(){const req={'name':org_delete_name};org_delete_name='';$.post('/orgs/delete',req,org_delete_fn);}
function clear_form(form){const prefix=form['field_element_prefix'];form['fields_clear'].forEach(function(field,index){$(prefix+field).val('');$(prefix+field).removeClass('is-invalid');$(prefix+field+'-feedback').hide('is-invalid');});}
function send_request_keypress(ev,form){if(ev.keyCode==13){ev.preventDefault();send_request(form);}}
function send_request(form){const prefix=form['field_element_prefix'];var req={};form['fields'].forEach(function(field,index){if($(prefix+field).length){req[field]=$(prefix+field).val();}});$.ajax({type:'POST',url:form['endpoint'],data:req,error:(jqXHR,textStatus,errorThrown)=>process_errors(form,jqXHR.responseJSON['errors']),success:resp=>process_success(form,resp['success']),dataType:'json'});}
function process_errors(form,errors){const prefix=form['field_element_prefix'];form['fields'].forEach(function(field,index){if(errors.hasOwnProperty(field)){$(prefix+field).addClass('is-invalid');$(prefix+field+'-feedback').html(errors[field]);$(prefix+field+'-feedback').show();}else{$(prefix+field).removeClass('is-invalid');$(prefix+field+'-feedback').hide();}});}
function process_success(form,resp){location.reload();}