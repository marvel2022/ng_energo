// console.log("Hello World")

// function base_js_function(e){	
// 	email = document.getElementById('subscriber-email').value;
// 	console.log(email)

// 	e.preventDefault();

// 	if (email.length > 0 ){
// 	  EmailValidation(email);
// 	  console.log("Calls EmailValidation Function");
// 	  document.getElementById('subscriber-email').value = '';
// 	}else{
// 	  console.log("Please enter a valid email address.");
// 	  alert("Please enter a valid email address.");
// 	  document.getElementById('subscriber-email').value = '';
// 	}  
// }
  
//   function EmailValidation(email){
// 	console.log('Email validation method - ' + email.toString());
  
// 	var url = '/subscription/';
  
// 	fetch(url, {
// 	  method:'POST',
// 	  headers:{
// 		'Content-Type':'application/json',
// 		'Accept': 'application/json',
// 		'X-CSRFToken':csrftoken,
// 	  }, 
// 	  body:JSON.stringify({'email':email})
// 	})
// 	.then((response) => {
// 	   return response.json();
// 	})
// 	.then((data) => {
// 	  console.log(data['action'])
// 	  if (data['action'] == 'not_valid'){
// 		  alert("Пожалуйста, введите действительный адрес электронной почты :(")
// 	  }else{
// 		  alert('Спасибо за подписку :)')
// 	  }
// 	});
//   }
  


