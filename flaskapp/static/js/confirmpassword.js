var password=document.getElementById("inputPassword"), confirm_password=document.getElementById("confirmPassword");
function validatepassword(){
    if (password.value != confirm_password.value){
        confirm_password.setCustomValidity("Password don't Match");
    }
    else{
        confirm_password.setCustomValidity();
    }
}



password.onchange = validatepassword();
confirm_password.onkeyup = validatepassword();