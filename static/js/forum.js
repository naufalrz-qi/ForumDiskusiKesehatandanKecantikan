function post() {
    let title = $("#input_title").val()
    let question = $("#input_question").val()
    let topic = $("#select_topic").val()
    let file = $("#input_pic")[0].files[0]

    let form_data = new FormData();
    let today = new Date().toISOString()
    form_data.append("title_give", title);
    form_data.append("question_give", question);
    form_data.append("topic_give", topic);
    form_data.append("file_give", file);
    form_data.append("date_give", today);
    console.log(form_data);
    $.ajax({
        type: "POST",
        url: "/posting",
        data:form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["result"] === "success") {
                alert(response["msg"]);
                window.location.replace('/')
              }
            
        }
    })
}

  function get_posts2() {
    
    username = '';
  
    $.ajax({
      type: "GET",
      url: `/get_posts?username_give=${username}`,
      data: {},
      success: function (response) {
        if (response["result"] === "success") {
          let posts = response["posts"];
          for (let i = 0; i < 3; i++) {
            let post = posts[i];
            let html_temp = `
    
            <li><a href="/${post['_id']}" class="h6 has-text-link">${post['title']}</a></li>


            
            `;
            $("#must-read").append(html_temp);    
          }
          for (let i = 4; i < 6; i++) {
            let post = posts[i];
            let html_temp2 = `
    
            <li><a href="/${post['_id']}" class="h6 has-text-link">${post['title']}</a></li>


            
            `;
            $("#popular-posts").append(html_temp2); 
          }
        }
      },
    });
  }

function get_posts(username) {

    if (username === undefined){
        username = '';
    }

    $.ajax({
      type: "GET",
      url: `/get_posts?username_give=${username}`,
      data: {},
      success: function (response) {
        if (response["result"] === "success") {
          let posts = response["posts"];
          for (let i = 0; i < posts.length; i++) {
            let post = posts[i];
            let time_post = new Date(post["date"]);
            let time_before = time2str(time_post);
            let class_heart = post['heart_by_me'] ? "fa-heart": "fa-heart-o"
            let class_star = post['star_by_me'] ? "fa-star": "fa-star-o"
            let class_thumbsup = post['thumbsup_by_me'] ? "fa-thumbs-up": "fa-thumbs-o-up"
            /*if (post["heart_by_me"]) {
                class_heart = "fa-heart"
            } else {
                class_heart = "fa-heart-o"
            }*/
            let html_temp = `
            
                <div class="card w-100 p-5 my-3" style="border-radius: 3%;">
                    <div class="card-body">
                        <div class="d-flex flex-row mb-4">
                            <a class="image is-48x48" href="/user/${post["username"]}">
                                <img class="is-rounded" src="/static/${post["profile_pic_real"]}"
                                    alt="Image">
                            </a>
                            <div class="d-flex flex-column mx-2">
                                <p class="m-0 p-0">
                                    <strong>${post["profile_name"]}</strong>                 
                                </p>
                                <p class="m-0 p-0">
                                <small>@${post["username"]}</small> <small>${time_before}</small>      
                                </p>   
                            </div>
                        </div>
                        <hr class="separator" style="margin: 0%;">
                        <div class="mt-5">
                            <p class="h5 has-text-weight-bold">${post['title']}</p>
                            <p style="padding-bottom:5%;">${post['question']}</p>
                            <hr class="separator" style="margin:0%;">
                            <p class="mt-4">topic : <a class="btn btn-success" style="padding:5px; margin:0px;">${post['topic']}</a></p>  
                            <div class="d-flex justify-content-center">
                                <img src="../static/${post['post_pic_real']}" alt="" style="object-fit: contain; height: 300px;">
                            </div>
                        </div>
                    </div>
                </div>
            
            `;
            $(".content").append(html_temp);
          }
        }
      },
    });
  }

  function time2str(date) {
    let today = new Date();
    let time = (today - date) / 1000 / 60;  // minutes

    if (time < 60) {
        return parseInt(time) + " minutes ago";
    }
    time = time / 60;  // hours
    if (time < 24) {
        return parseInt(time) + " hours ago";
    }
    time = time / 24; // days
    if (time < 7) {
        return parseInt(time) + " days ago";
    }
    return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`;
}