function update_profile(user_role) {
    let name = $("#input-name").val();
    let file = $("#input-pic")[0].files[0];
    let info = $("#textarea-info").val();

    let form_data = new FormData();
    form_data.append("file_give", file);
    form_data.append("name_give", name);
    form_data.append("info_give", info);
    form_data.append("role", user_role);

  
    $.ajax({
      type: "POST",
      url: "/update_profile",
      data: form_data,
      cache: false,
      contentType: false,
      processData: false,
      success: function (response) {
        if (response["result"] === "success") {
          alert(response["msg"]);
          window.location.reload();
        }
      },
    });
  }