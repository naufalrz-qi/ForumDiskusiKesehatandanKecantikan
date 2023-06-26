function sign_in() {
    let username = $("#input_user").val();
    let password = $("#input_pass").val();

    if (username === "") {
      $("#help-user-login").text("Please input your username.");
      $("#input_user").focus();
      return;
    } else {
      $("#help-user-login").text("");
    }

    if (password === "") {
      $("#help-password").text("Please input your password.");
      $("#input_pass").focus();
      return;
    } else {
      $("#help-password-login").text("");
    }
    $.ajax({
      type: "POST",
      url: "/sign_in",
      data: {
        username_give: username,
        password_give: password,
      },
      success: function (response) {
        if (response["result"] === "success") {
          $.cookie("my_token", response["token"], { path: "/" });
          swal("Success","Login successful!", "success");

          window.location.replace("/");
        } else {
          swal("Failed",response["msg"], "error");

        }
      },
    });
  }