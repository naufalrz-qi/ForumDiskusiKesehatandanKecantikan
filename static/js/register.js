
document.getElementById("input_user").onchange = function() {check_dup()};

function sign_up() {
    let helpUser = $('#help_user')
    let inputPassword = $('#input_pass')
    let inputPassword2 = $('#input_pass2')
    let inputEmail = $('#input_email')
    let selectRole = $('#role_select')


    let username = $('#input_user').val();
    let email = inputEmail.val();
    let password = inputPassword.val();
    let password2 = inputPassword2.val();
    let role = selectRole.val()
    
    if (helpUser.hasClass('is-danger')){
        swal("Failed","Please check your username", "error");
        return;
    }else if(!helpUser.hasClass('is-success')){
        swal("Failed","Please check your username again, something is wrong", "error");
        return;
    }

    let helpPassword = $('#help_pass')
    let helpPassword2 = $('#help_pass2')
    let helpRole = $('#help_role')

    

    if (password === ''){
        helpPassword.text('Please enter your password')
                    .removeClass('is-safe')
                    .addClass('is-danger')
        inputPassword.focus()
        return;
    }else if (!is_password(password)){        
        helpPassword.text('For your password, please enter 8-20 English characters, numbers, or the following special characters (!@#$%^&*)')
                    .removeClass('is-safe')
                    .addClass('is-danger')
        inputPassword.focus()
        return;
    }else{
        helpPassword.text('This password can be used!')
                    .removeClass('is-danger')
                    .addClass('is-success')
    }


    if (password2 === ''){
        helpPassword2.text('Please enter your password')
                    .removeClass('is-safe')
                    .addClass('is-danger')
        inputPassword2.focus()
        return;
    } else if(password2 != password){
        helpPassword2.text("Password doesn't match")
                    .removeClass('is-safe')
                    .addClass('is-danger')
        inputPassword2.focus()
        return;
    }

    if(role === ''){
        helpRole.text('Please select one of them between normal user or an expert')
        .removeClass('is-safe')
        .addClass('is-danger')
        selectRole.focus()
        return;
    }

    $.ajax({
        type: "POST",
        url: "/sign_up/save",
        data: {
        username_give: username,
        email_give: email,
        password_give: password,
        role_give: role,

        },
        success: function (response) {
        if(response["result"] == 'success'){
            swal("Success","Your username has been registered", "success");
            window.location.replace("/login");
        }else{
            swal("Failed","Something went wrong", "error");
        }
        
        },
    });
    }

function is_username(asValue) {
    var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{5,15}$/;
    return regExp.test(asValue);
}

function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}

function check_dup(){
    let inputUsername = $('#input_user')
    let helpUser = $('#help_user')
    let username = inputUsername.val()
    if (username === ''){
        helpUser.text("Please enter your username")
                .removeClass('is-safe')
                .addClass('is-danger')
        inputUsername.focus();
        return;
    }

    if (!is_username(username)){
        helpUser.text("For your username, please type in 5-15 English characters, numbers, or special characters(._-)")
                .removeClass('is-safe')
                .addClass('is-danger');
        inputUsername.focus();
        return;
    }

    helpUser.addClass('is-loading');

    $.ajax({
        type:'POST',
        url:'/sign_up/check_dup',
        data:{
            username_give:username,
        },
        success: function(response){
            if (response['exists']){
                helpUser.text('This is already in use')
                        .removeClass('is-safe')
                        .addClass('is-danger')
                inputUsername.focus()
            }else{
                helpUser.text('This username is available for use!')
                        .removeClass('is-danger')
                        .addClass('is-success')
            }
            helpUser.removeClass('is-loading')
        }
    })
}