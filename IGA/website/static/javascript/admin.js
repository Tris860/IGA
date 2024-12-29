
setInterval(() => {
  Requests();
  Users();
  myposts()
  Content();
  myaccount_details();
  },1000)

function toggleForm() {
    const popup_window=document.getElementById('popups');
    const closeButton = document.getElementById('closeButton');
    const profileinfo = document.getElementById('proinfo');
    var division =document.getElementsByClassName('div-to-hide');
  
    if (popup_window.style.display === 'block') {
      profileinfo.style.display = 'none';
      popup_window.style.display='none'
      for (let index = 0; index < division.length; index++) {
           division[index].style.display='none';
        }
    } else {
      popup_window.style.display='block'
      profileinfo.style.display = 'block';
    }
}
function toggleForms(sup) {
  console.log(sup)
  const popup_window=document.getElementById('popups');
  var division =document.getElementsByClassName('div-to-hide');
  for (let index = 0; index < division.length; index++) {
    division[index].style.display='none';
  }
  const divisionContent=document.getElementsByClassName('div-to-hide')[sup];
  divisionContent.style.display='block';
  
}
function hide_popupBox(){
  document.getElementById('popups').style.display='none';
}
function approve(email) {
  fetch('/approve', {
    method: 'POST',
    headers:{
      'Content-Type': 'application/json'
    },
    body:JSON.stringify({email: email})
  })
  .then(response => response.json())
    .then(data => {
        // Display the response message
        message_toggle(data)
        // document.getElementById('content').innerText = data;
    })
    .catch(error => console.log('Error:', error));
  
 }
function message_toggle (data) {
  if('Error' in data){
    const userDiv = document.getElementById('message_box');
    userDiv.classList.add('message_error');
    userDiv.innerHTML=`<h3>${data.Error}</h3>`;
    userDiv.style.display="block";
    setTimeout(() => {
        userDiv.style.animation="fade_box 1.5s ease ";
        userDiv.addEventListener('animationend',() => {
          userDiv.style.display='none'
        })
    }, 10000);
  } 
 }
 function message_toggle_settings (data) {
  if('Error' in data){
    const userDiv = document.getElementById('message_credential');
    userDiv.classList.add('message_error');
    userDiv.innerHTML=`<h3>${data.Error}</h3>`;
    userDiv.style.display="block";
    setTimeout(() => {
        userDiv.style.animation="fade_box 1.5s ease ";
        userDiv.addEventListener('animationend',() => {
          userDiv.style.display='none'
        })
    }, 10000);
    
 }
 else{
   const userDiv = document.getElementById('message_credential');
   userDiv.classList.add('message_success');
   userDiv.innerHTML=`<h3>${data.Success}</h3>`;
   userDiv.style.display="block";
    setTimeout(() => {
        userDiv.style.animation="fade_box 1.5s ease ";
        userDiv.addEventListener('animationend',() => {
          userDiv.style.display='none'
        })
    }, 5000);
   Requests()
 }
}
function displayNotification(message) {
  // Create a notification eleee
  const notification = document.createElement('div');
  notification.classList.add('notification');
  notification.textContent = message;

  // Append the notification to the notification zone
  document.getElementById('notification-zone').appendChild(notification);

  // Optionally, add a timeout to remove the notification after a certain time
  setTimeout(() => {
      notification.remove();
  }, 5000); // Remove after 5 seconds
}

function showDiv(divId,Id) {
  document.querySelectorAll('.panel').forEach(a => {
    a.classList.add('inactive');
  })
  document.querySelectorAll('.table').forEach(tables => {
    tables.classList.add('searchable');
  })
  document.querySelectorAll('.table').forEach(tables => {
    tables.classList.remove('searchable');
  })
document.getElementsByClassName('table')[Id].classList.add('searchable');
 

  document.querySelectorAll('.box').forEach(div => {
    div.classList.add('hidden');
  });
  document.getElementsByClassName('table')[Id].classList.remove('unsearchable');
  document.getElementsByClassName('panel')[Id].classList.remove('inactive');
  document.getElementById(divId).classList.remove('hidden');
}
function disapprove(email) {
  fetch('/disapprove', {
    method: 'POST',
    headers:{
      'Content-Type': 'application/json'
    },
    body:JSON.stringify({email: email})
  })
  .then(response => response.json())
    .then(data => {
        // Display the response message
        message_toggle(data)
        // document.getElementById('content').innerText = data;
    })
    .catch(error => console.log('Error:', error));
  
 }
function block(email) {
  fetch('/block_user', {
    method: 'POST',
    headers:{
      'Content-Type': 'application/json'
    },
    body:JSON.stringify({email: email})
  })
  .then(response => response.json())
    .then(data => {
        // Display the response message
        message_toggle(data)
        // document.getElementById('content').innerText = data;
    })
    .catch(error => console.log('Error:', error));
}
function activate_user(email) {
  fetch('/activate_user', {
    method: 'POST',
    headers:{
      'Content-Type': 'application/json'
    },
    body:JSON.stringify({email: email})
  })
  .then(response => response.json())
    .then(data => {
        // Display the response message
        message_toggle(data)
        // document.getElementById('content').innerText = data;
    })
    .catch(error => console.log('Error:', error));
}
function delete_account(email) {
  
}
function myaccount_details2(){
  var  email =document.getElementById('user_email').innerText
  userDataDiv=document.getElementById('myinfo')
  console.log(email)
  fetch('/mycredentials',{
      method: 'POST',
      headers: {
          'Content-Type' : 'application/json'
      },
      body:JSON.stringify({email : email})
  })
  .then(response => response.json())
  .then(data => {
      if('Error' in data ){
          userDataDiv.innerHTML=''
          userDataDiv.innerHTM=`<span style='color:red;'>${data.Error}</span>`;
       }
       else{
          data.forEach(user => { 
              userDataDiv.innerHTML = 
                 `<span>${user.username}</span> 
                 <span id="email_account"> ${user.email}</span>
                  `;
               }); 
       }
  })
}
function change(field,value) {
  document.getElementById('form_change').style.display='block';
  document.getElementById('files_posted_container').style.display='none';
  var h3=document.getElementById('form_change_title');
  document.getElementById('field').innerText =field
  document.getElementById('field_name').innerText =field
  document.getElementById('nameField').value =field
  document.getElementById('field_value').value =value
}
function close_change_form(){
  document.getElementById('form_change').style.display='none';
  document.getElementById('files_posted_container').style.display='block';
}

function change_field() {
  field=document.getElementById('nameField').value;
  value=document.getElementById('field_value').value;
  acc_email=document.getElementById('user_email').innerText;
  close_change_form()
  fetch('/change_credentions',{
    method:'POST',
    headers:{
      'Content-Type':'application/json'
    },
    body:JSON.stringify({field_name:field, field_value:value, email:acc_email})
  })
  .then(response => response.json())
  .then(data =>{
      message_toggle_settings(data)
      myaccount_details();
  })
  .catch(error => console.log('Error:', error));
}
