let level=null;
let subject=null;
function subject_selector(lesson) {
    var lesson_Selected=lesson;
    subject=lesson;
    Sorter(level=level,subject=lesson_Selected)
}
function level_selector(grade) {
    var level_Selected=grade;
    level=level_Selected;
    Sorter(level=level_Selected,subject=subject)
}
function Sorter(level=null,subject=null) {
    fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: level ,lesson: subject})
    })
    .then(response => response.json())
    .then(data => {
        // Display the response message
        document.getElementById('response').innerText = data.message;
    })
    .catch(error => console.error('Error:', error));
}
function Content_Books(){
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: level ,lesson: subject})
    })
    .then(response => response.json())
    .then(data => {
        // Display the response message
        document.getElementById('response').innerText = data.message;
    })
    .catch(error => console.error('Error:', error));
}
function displayRequest(data) { 
    const userDataDiv = document.getElementById('request_table'); 
    userDataDiv.innerHTML = ''; // Clear any existing content
     // Loop through each user and create an HTML representation 
     if('message' in data ){
        const userDiv = document.createElement('div');
        userDiv.classList.add('Message');
        userDiv.innerHTML=`<h3>${data.message}</h3>`;
        userDataDiv.appendChild(userDiv);
     }
     else{
        data.forEach(user => { 
            const userDiv = document.createElement('tr'); 
            userDiv.innerHTML = 
               `
                <td class="notification">
                    <p>${user.username}</p>
                    <div class="notibuttons">
                        <button id="approve"    onclick="approve('${user.email}')" >Approve</button>
                        <button id="disapprove" onclick="disapprove('${user.email}')">Disapprove</button>
                    </div>
                    <div id="notificationinfo">
                        <strong>Username:</strong><p>${user.username}</p>
                        <strong>Email: </strong><p>${user.email}</p>  
                    </div>  
                </td>
                `;
              userDataDiv.appendChild(userDiv);
             }); 
     }
     
}
function displayContent(data) { 
    const userDataDiv = document.getElementById('request_table2'); 
    userDataDiv.innerHTML = ''; // Clear any existing content
     // Loop through each user and create an HTML representation 
     if('message' in data ){
        const userDiv = document.createElement('div');
        userDiv.classList.add('Message');
        userDiv.innerHTML=`<h3>${data.message}</h3>`;
        userDataDiv.appendChild(userDiv);
     }
     else{
        data.forEach(user => { 
            const userDiv = document.createElement('tr'); 
            userDiv.innerHTML = 
               `
                <td class="notification">
                    <p>${user.title}</p>
                    <div class="notibuttons">
                        <button id="approve">Approve</button>
                        <button id="disapprove">Disapprove</button>
                    </div>
                    <div id="notificationinfo">
                        <strong>level: </strong><p>${user.level}</p>  
                        <strong>lesson: </strong><p>${user.lesson}</p>  
                        <strong>location: </strong><p>${user.link}</p>
                    </div>  
                </td>
                `;
              userDataDiv.appendChild(userDiv);
             }); 
     }
     
}
function displayUsers(data) { 
    const userDataDiv = document.getElementById('request_table3'); 
    userDataDiv.innerHTML = ''; // Clear any existing content
    if('message' in data){
        const userDiv = document.createElement('div');
        userDiv.classList.add('Message');
        userDiv.innerHTML=`<h3>${data.message}</h3>`;
        userDataDiv.appendChild(userDiv);
     }
     else{
        data.forEach(user => { 
            const userDiv = document.createElement('tr'); 
            if (user.status == true){
                userDiv.innerHTML = 
                    `
                    <td class="notification active_user" >
                        <p>${user.username}</p>
                        <div class="notibuttons">
                             
                             <button id="block"    onclick="block('${user.email}')">Block</button>
                             <button id="delete"   onclick="delete('${user.email}')">Delete</button>
                        </div>
                        <div id="notificationinfo">
                             <strong>Username: </strong><p>${user.username}</p>
                             <strong>Email: </strong><p>${user.email}</p>  
                         </div>  
                    </td>
                   `;

            }
            else if(user.status == false){
                userDiv.innerHTML = 
                    `
                    <td class="notification blocked_user">
                        <p>${user.username}</p>
                        <div class="notibuttons">
                             <button id="activate" onclick="activate_user('${user.email}')">Activate</button>
                             <button id="delete"   onclick="delete('${user.email}')">Delete</button>
                        </div>
                        <div id="notificationinfo">
                             <strong>Username: </strong><p>${user.username}</p>
                             <strong>Email: </strong><p>${user.email}</p>  
                         </div>  
                    </td>
                   `;

            }
              userDataDiv.appendChild(userDiv);
             }); 
     }
 }        
function Requests(){
    level=0,lesson=9
    fetch('/request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: level ,lesson: subject})
    })
    .then(response => response.json())
    .then(data => {
        // Display the response message
        displayRequest(data);
        // document.getElementById('content').innerText = data;
    })
    .catch(error => console.log('Error:', error));
}
function Content(){
    
    fetch('/content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },  
    })
    .then(response => response.json())
    .then(data => {
        // Display the response message
        displayContent(data);
    })
    .catch(error => console.log('Error:', error));
}
function Users(){
    
    fetch('/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },  
    })
    .then(response => response.json())
    .then(data => {
        // Display the response message
        displayUsers(data);
    })
    .catch(error => console.log('Error:', error));
}
function Search() {
    var input, filter, table, li, a, i, txtValue;
    input = document.getElementById("searchbar");
    filter = input.value.toUpperCase();
    table = document.querySelector(".searchable");
    li = table.getElementsByTagName("tr");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("td")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function myposts(){
    var  email =document.getElementById('user_email').innerText
    var userDataDiv=document.getElementById('files_posted')
    
    fetch('/myposts',{
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json'
        },
        body:JSON.stringify({email : email})
    })
    .then(response => response.json())
    .then(data => {
        if('message' in data ){
            userDataDiv.innerHTML=''
            const userDiv = document.createElement('div');
            userDiv.classList.add('Message');
            userDiv.innerHTML=`<h3 style='color:black;'>${data.message}</h3>`;
            userDataDiv.appendChild(userDiv);
         }
         else{
            data.forEach(user => { 
                const userDiv = document.createElement('h1'); 
                userDiv.innerHTML = `hello`;
                userDataDiv.appendChild(userDiv);
                 }); 
         }
    })
}
function myaccount_details(){
    var  email =document.getElementById('user_email').innerText
    userDataDiv=document.getElementById('myinfo')
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

function upload_file() {
    var email=document.getElementById('email').innerText;
    var level=document.getElementById('level').value;
    var lesson=document.getElementById('lesson').value;
    var title =document.getElementById('title').value;
    var fileInput = document.getElementById('link'); 
    var usernameInput = document.getElementById('username');

    var formData = new FormData();

    formData.append('file', fileInput.files[0]); 
    formData.append('username', usernameInput.value);
    formData.append('lesson', lesson);
    formData.append('level', level);
    formData.append('email', email);
    formData.append('title', title);

    var xhr = new XMLHttpRequest();
    
    xhr.open('POST', '/upload', true);
    xhr.onload = function () { 
        if (xhr.status === 200) { 
            alert('File uploaded successfully'); 
        } 
        else {
             alert('Error uploading file'); 
            } 
        };
     xhr.send(formData);
}