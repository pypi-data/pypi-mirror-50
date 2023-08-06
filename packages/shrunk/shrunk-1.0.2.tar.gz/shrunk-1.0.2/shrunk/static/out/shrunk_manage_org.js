var shrunk=shrunk||function(){}
var clear_search=function(){var url=new URL(window.location.href);var sortBy=url.searchParams.get("sortby");var all_users=url.searchParams.get("all_users");if(sortBy===null){sortBy="0"}
if(all_users===null){all_users=1;}
window.location.replace("/?all_users="+all_users+"&search=&sortby="+sortBy);}
function toggleLinks(cb,netid){$("article.link-group").each(function(){if(cb.checked)
$(this).css("display","block");else{link_info=$(this).children(".link-info");if($(link_info).children(".owner").attr("netid")!=netid)
$(this).css("display","none");}});}
const CSRF_TOKEN=$('meta[name=csrf-token]').attr('content');$.ajaxSetup({beforeSend:function(xhr,settings){xhr.setRequestHeader('X-CSRFToken',CSRF_TOKEN);}});const ADD_MEMBER_FORM={'endpoint':'/orgs/add_member','field_element_prefix':'#member-add-','fields':['name','netid','is_admin'],'fields_clear':['netid','is_admin']};function add_member_keypress(ev){if(ev.keyCode==13){ev.preventDefault();add_member_shim();}}
function add_member_shim(){if($('#member-add-is_admin-checkbox').is(':checked')){$('#member-add-is_admin').val('true');}else{$('#member-add-is_admin').val('');}
send_request(ADD_MEMBER_FORM);}
var remove_member_org_name;var remove_member_netid;var remove_member_cont;function remove_member(ev){var parent=ev.target.parentElement;if(parent.tagName=='BUTTON')
parent=parent.parentElement;remove_member_org_name=parent.querySelector('.org-name').value;remove_member_netid=parent.querySelector('.org-member-netid').value;if(remove_member_netid==$('#netid').val())
remove_member_cont=()=>location.replace('/');else
remove_member_cont=()=>location.reload();$('#delete-member-header').text('Are you sure you want to remove this member?');$('#delete-member-message').text('This operation cannot be undone.').css('color','black');$('#delete-member-button').html('Delete');$('#member-remove-modal').modal();}
function remove_self(){remove_member_org_name=$('#org_name').val();remove_member_netid=$('#netid').val();remove_member_cont=()=>location.replace('/');$('#delete-member-header').text('Are you sure you want to leave this organization?');$('#delete-member-message').text('This operation cannot be undone.').css('color','black');$('#delete-member-button').html('Leave');$('#member-remove-modal').modal();}
function do_remove_member(){const req={'name':remove_member_org_name,'netid':remove_member_netid};$.ajax({type:'POST',url:'/orgs/remove_member',data:req,error:(jqXHR,textStatus,errorThrown)=>remove_member_error(jqXHR),success:remove_member_cont});}
function remove_member_error(jqXHR){const err=jQuery.parseJSON(jqXHR.responseText)['error'];$('#delete-member-message').text(err).css('color','red');}
var org_delete_name;var org_delete_fn;function delete_org_list(ev){var parent=ev.target.parentElement;if(parent.tagName=='BUTTON')
parent=parent.parentElement;org_delete_name=parent.querySelector('.org-name').value;org_delete_fn=function(){location.reload();};$('#org-delete-modal').modal();}
function delete_org_manage(name){org_delete_name=name;org_delete_fn=function(){window.location.replace('/orgs');};$('#org-delete-modal').modal();}
function do_delete_org(){const req={'name':org_delete_name};org_delete_name='';$.post('/orgs/delete',req,org_delete_fn);}
function clear_form(form){const prefix=form['field_element_prefix'];form['fields_clear'].forEach(function(field,index){$(prefix+field).val('');$(prefix+field).removeClass('is-invalid');$(prefix+field+'-feedback').hide('is-invalid');});}
function send_request_keypress(ev,form){if(ev.keyCode==13){ev.preventDefault();send_request(form);}}
function send_request(form){const prefix=form['field_element_prefix'];var req={};form['fields'].forEach(function(field,index){if($(prefix+field).length){req[field]=$(prefix+field).val();}});$.ajax({type:'POST',url:form['endpoint'],data:req,error:(jqXHR,textStatus,errorThrown)=>process_errors(form,jqXHR.responseJSON['errors']),success:resp=>process_success(form,resp['success']),dataType:'json'});}
function process_errors(form,errors){const prefix=form['field_element_prefix'];form['fields'].forEach(function(field,index){if(errors.hasOwnProperty(field)){$(prefix+field).addClass('is-invalid');$(prefix+field+'-feedback').html(errors[field]);$(prefix+field+'-feedback').show();}else{$(prefix+field).removeClass('is-invalid');$(prefix+field+'-feedback').hide();}});}
function process_success(form,resp){location.reload();}