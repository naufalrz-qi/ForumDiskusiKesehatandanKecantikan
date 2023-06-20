function verify_expert(id,user_id){
    console.log(user_id)
    $.ajax({
        type: "POST",
        url: "/verifying",
        data: {
            id:id,
            user_id:user_id
        },
        success: function (response) {
          if (response["result"] === "success") {
            alert(response["msg"]);
            window.location.reload();
          }
        },
      });
}