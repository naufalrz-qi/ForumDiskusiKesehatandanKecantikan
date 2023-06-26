function update_profile(user_role) {
    let name = $("#input-name").val();
    let file = $("#input-pic")[0].files[0];
    let info = $("#textarea-info").val();

    let form_data = new FormData();
    if(user_role === 'normal'){
      form_data.append("file_give", file);
      form_data.append("name_give", name);
      form_data.append("info_give", info);
      form_data.append("role", user_role);
    }

    if(user_role==='expert'){
      let gender = $("#input-gender").val();
      let academic_info = $("#input-acinfo").val();
      let workplace = $("#input-workplace").val();
      let service = $("#input-service").val();
      let phone_number = $("#input-number").val();
      
      form_data.append("file_give", file);
      form_data.append("name_give", name);
      form_data.append("gender_give", gender);
      form_data.append("academic_give", academic_info);
      form_data.append("workplace_give", workplace);
      form_data.append("service_give", service);
      form_data.append("number_give", phone_number);
      form_data.append("info_give", info);
      form_data.append("role", user_role);

    }
  
    $.ajax({
      type: "POST",
      url: "/update_profile",
      data: form_data,
      cache: false,
      contentType: false,
      processData: false,
      success: function (response) {
        if (response["result"] === "success") {
          swal("Success",response["msg"], "success");
          window.location.reload();
        }
      },
    });
  }

