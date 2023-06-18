function post() {
    let title = $("#input_title").val()
    let input_question = $("#input_question").val()
    let topic = $("#select_topic").val()
    let file = $("#input_pic")[0].files[0]

    let paragraph = input_question.split("\n")
    let question = ""
    for(let i = 0; i<paragraph.length; i++){
      question += paragraph[i]+"<br>";
    }
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
function answer(id_post) {
    let input_answer = $("#textarea-answer").val()
    let file = $("#input_answer_pic")[0].files[0]
    let paragraph = input_answer.split("\n")
    let answer = ""
    for(let i = 0; i<paragraph.length; i++){
      answer += paragraph[i]+"<br>";
    }
    let form_data = new FormData();
    let today = new Date().toISOString()
    form_data.append("id_post", id_post);
    form_data.append("answer_give", answer);
    form_data.append("file_give", file);
    form_data.append("date_give", today);
    console.log(form_data);
    $.ajax({
        type: "POST",
        url: "/answering",
        data:form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["result"] === "success") {
                alert(response["msg"]);

                //you should direct the user into discussion details
                window.location.replace('/')
              }
            else if(response["result"] === 'failed'){
              alert(response['msg'])
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
    
            <li><a href="/${post['_id']}" class="h6 has-text-link" style="font-size: 14px; ">${post['title']}</a></li>


            
            `;
            $("#must-read").append(html_temp);    
          }
          for (let i = 4; i < 6; i++) {
            let post = posts[i];
            let html_temp2 = `
    
            <li><a href="/${post['_id']}" class="h6 has-text-link" style="font-size: 14px; ">${post['title']}</a></li>


            
            `;
            $("#popular-posts").append(html_temp2); 
          }
        }
      },
    });
  }

function get_posts(username) {

    $("#discussion").empty();

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
            let id= post['_id']
            let time_post = new Date(post["date"]);
            
            showPost(post, time_post)
            getAnswer(id)
          }
        }
      },
    });
  }

  function showPost(post, time_post) {  
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
            <p><a class="btn btn-success p-1 m-0" style="font-size:10px;">${post['topic']}</a></p>
            <p class="h4 has-text-weight-bold">${post['title']}</p>
                <div class="d-flex flex-row mb-4">
                    <a class="image is-48x48" href="/user/${post["username"]}">
                        <img class="is-rounded" src="../static/${post["profile_pic_real"]}"
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
                
                <div class="mt-5">
                    <p style="padding-bottom:5%;">${post['question']}</p>
                    
                      
                    <div class="d-flex justify-content-center">
                        <img src="../static/${post['post_pic_real']}" alt="" style="object-fit: contain; height: 300px;">
                    </div>
                </div>
            </div>

            
            <hr class="separator m-0 mb-3 p-0">
            <section id="answer">
              <p class="h6">Answer Section</p>
              <article class="media">
                  <div class="media-content my">
                      <div class="field">
                          <p class="control">
                              <input 
                              id="input-answer"
                              class="input is-rounded"
                              placeholder="What are you thinking about?"
                              onclick="$('#modal-answer-${post['_id']}').addClass('is-active')"
                              />

                              <div class="modal" id="modal-answer-${post['_id']}">
                                  <div class="modal-background" onclick='$("#modal-answer-${post['_id']}").removeClass("is-active")'></div>
                                  <div class="modal-content">
                            
                                          <article class="media">
                                              <div class="media-content p-5">
                                                  <div class="field">
                                                      <p class="control">
                                                          <textarea id="textarea-answer" class="textarea"
                                                                    placeholder="Answer the question"></textarea>
                                                      </p>
                                                  </div>
                                                  <div class="field control is-expanded">
                                            <label class="label">Add image</label>
                                            <div class="file has-name py-2">
                                              <label class="file-label" style="width: 100%">
                                                <input
                                                  id="input_answer_pic"
                                                  class="file-input"
                                                  type="file"
                                                  name="resume"
                                                />
                                                <span class="file-cta"
                                                  ><span class="file-icon"
                                                    ><i class="fa fa-upload"></i
                                                  ></span>
                                                  <span class="file-label">Select a file</span>
                                                </span>
                                                <span
                                                  id="file_name"
                                                  class="file-name"
                                                  style="width: 100%; max-width: 100%"
                                                  ></span
                                                >
                                              </label>
                                            </div>
                                          </div>
                                                  <nav class="level is-mobile">
                                                      <div class="level-right">
                                                          <div class="level-item">
                                                              <a class="button is-primary" onclick="answer('${post['_id']}')">Answer</a>
                                                          </div>
                                                          <div class="level-item">
                                                              <a class="button is-primary is-outlined"
                                                                onclick='$("#modal-answer-${post['_id']}").removeClass("is-active")'>Cancel</a>
                                                          </div>
                                                      </div>
                                                  </nav>
                                              </div>
                                          </article>
                                      
                                  </div>
                                  <button class="modal-close is-large" aria-label="close"
                                          onclick='$("#modal-answer-${post['_id']}").removeClass("is-active")'></button>
                              </div>

                          </p>
                      </div>
                  </div>
              </article>
              <div id="answer-${post['_id']}">
                 
              </div>
            </section>
        </div>
        
    `;
    $("#discussion").append(html_temp);
  }
  function getAnswer(postID) {
    $.ajax({
    type:"POST",
    url:'/get_answers',
    data:{'id_post':postID},
    success:function(response){
      if (response["result"] === "success") {
        let answers = response["answers"];
        console.log(response['answers'])
        if(answers.length>0){
        for (let i = 0; i < answers.length; i++) {
            let answer = answers[i];
            let time_answer = new Date(answer["date"]);
            let time_before2 = time2str(time_answer);
            let answer_temp =
                `
                <div class="w-100">
                <div>
                    <div class="d-flex flex-row mb-4">
                        <a class="image is-48x48" href="/user/${answer["username"]}">
                            <img class="is-rounded" src="../static/${answer["profile_pic_real"]}"
                                alt="Image">
                        </a>
                        <div class="card d-flex flex-column mx-2 p-3 w-100" >
                            <p class="m-0 p-0">
                                <strong>${answer["profile_name"]}</strong>                 
                            </p>
                            <p class="m-0 p-0">
                            <small>@${answer["username"]}</small> <small>${time_before2}</small>      
                            </p>
                          
                            <p style="padding-bottom:5%;">${answer['answer']}</p>
                          
                        </div>
                    </div>
                
                </div> 
                `
            $(`#answer-${postID}`).append(answer_temp);

          }
        }
        else if(answers.length>3){
          for (let i = 0; i < 3; i++) {
              let answer = answers[i];
              let time_answer = new Date(answer["date"]);
              let time_before2 = time2str(time_answer);
              let answer_temp =
                  `
                  <div class="w-100">
                  <div>
                      <div class="d-flex flex-row mb-4">
                          <a class="image is-48x48" href="/user/${answer["username"]}">
                              <img class="is-rounded" src="../static/${answer["profile_pic_real"]}"
                                  alt="Image">
                          </a>
                          <div class="card d-flex flex-column mx-2 p-3 w-100">
                              <p class="m-0 p-0">
                                  <strong>${answer["profile_name"]}</strong>                 
                              </p>
                              <p class="m-0 p-0">
                              <small>@${answer["username"]}</small> <small>${time_before2}</small>      
                              </p>
                            
                              <p style="padding-bottom:5%;">${answer['answer']}</p>
                            
                          </div>
                      </div>
                  
                  </div> 
                  `

            $(`#answer-${postID}`).append(answer_temp);
                
            }
          }
      }
    }

  })  }

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