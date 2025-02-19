const signUpUsername=document.getElementById("sign-up-username")
const signUpEmail=document.getElementById("sign-up-email")
const setPassword=document.getElementById("set-password")
const signUpBtn=document.getElementById("sign-up-button")
let i=0

signUpUsername.addEventListener('keydown',(event)=>{
    if(event.key=='Enter')
        signUpEmail.focus()
})
signUpEmail.addEventListener('keydown',(event)=>{
    if(event.key=='Enter')
        setPassword.focus()
})


const loginEmail=document.getElementById("email")
const password=document.getElementById("password")
const loginBtn=document.getElementById("log-in-button")
const errorMessage=document.getElementById("error-message")


loginEmail.addEventListener('keydown',(event)=>{
    if(event.key=='Enter'){
        password.focus()
    }
   
})