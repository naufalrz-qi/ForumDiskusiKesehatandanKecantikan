function edit(id_post, id_user) {
    let title = $("#input_title").val()+'[edited]'
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
    form_data.append("id_post", id_post);
    form_data.append("id_user", id_user);
    form_data.append("title_give", title);
    form_data.append("question_give", question);
    form_data.append("topic_give", topic);
    form_data.append("file_give", file);
    form_data.append("date_give", today);
    console.log(form_data);
    $.ajax({
        type: "POST",
        url: "/post_editing",
        data:form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["result"] === "success") {
                alert(response["msg"]);
                window.location.replace('/')
              }
              else if (response["result"] === "failed") {
                alert(response["msg"]);
                window.location.replace('/')
              }
            
        }
    })
}

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
    let input_answer = $("#textarea-answer-"+id_post).val()
    let file = $("#input_answer_pic_"+id_post)[0].files[0]
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
                window.location.reload()
              }
            else if(response["result"] === 'failed'){
              alert(response['msg'])
            }
            
        }
    })
}

  function get_posts2() {
    
    let username = '';
  
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
    console.log(username )
    if (username === undefined){
        username = '';
    

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
  else{
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
  }

  function confirmDelete(postId) {
    if (confirm("Are you sure you want to delete this post?")) {
      // Jika pengguna menekan "OK" pada dialog konfirmasi, maka hapus postingan
      window.location.href = "/delete/" + postId;
    }
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
    const username = $('script[data-username]').data('username');
    let id_post = post['_id']
    let editPostHtml = '';
    if (post['username'] === username) {
    editPostHtml = `<a class="dropdown-item" href="/edit_post/${post['_id']}"><span>Edit post</span></a>
                    <a class="dropdown-item" href="#" onclick="confirmDelete('${post['_id']}')"><span>Delete Post</span></a>
    `;
    }

    let html_temp = `
    
        <div class="card w-100 p-3 my-3" style="border-radius: 30px;">
            <div class="card-body">
            <div class="d-flex flex-row mb-5">
            <div class="col-11">
              <a class="btn btn-success p-1 m-0" href="" style="font-size:10px; width: fit-content;">${post['topic']}</a>
            </div>
            <a class="bi bi-three-dots-vertical col-1 d-flex justify-content-end" onclick="$('#post_drop_${post['_id']}').toggleClass('is-active')" style="font-size: 18px; color: inherit;"></a>
            <div class="dropdown is-right" id="post_drop_${post['_id']}">
              <div class="dropdown-menu">
                <div class="dropdown-content">
                  ${editPostHtml}
                  <a class="dropdown-item" href="/post_detail/${post['_id']}"><span>View Detail</span></a>
                  <a class="dropdown-item" href="#" onclick="showReportModal('${post['_id']}')"><span>Report</span></a>
                </div>
              </div>
            </div>
            </div>

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
                    <p>${post['question']}</p>
                    
                      
                    <div class="d-flex justify-content-center">
                        <img src="../static/${post['post_pic_real']}" alt="" style="object-fit: contain; height: 300px;">
                    </div>
                </div>
            </div>

            
            <hr class="separator m-0 my-3 mx-5 p-0 px-5">
            <section id="answer" class="p-3">
              <p class="h6 has-text-weight-bold"><a class="text-body-secondary" href="/post_detail/${post['_id']}" >See another answer</a></p>
              <article class="media" style="margin-bottom:0px;">
                  <div class="media-content">
                      <div class="field">
                          <p class="control">
                              <input 
                              id="input-answer"
                              class="input is-rounded"
                              placeholder="Answer the question"
                              onclick="$('#modal-answer-${post['_id']}').addClass('is-active')"
                              />

                              <div class="modal" id="modal-answer-${post['_id']}">
                                  <div class="modal-background" onclick='$("#modal-answer-${post['_id']}").removeClass("is-active")'></div>
                                  <div class="modal-content">
                            
                                          <article class="media">
                                              <div class="media-content p-5">
                                                  <div class="field">
                                                      <p class="control">
                                                          <textarea id="textarea-answer-${post['_id']}" class="textarea"
                                                                    placeholder="Answer the question"></textarea>
                                                      </p>
                                                  </div>
                                                  <div class="field control is-expanded">
                                            <label class="label">Add image</label>
                                            <div class="file has-name py-2">
                                              <label class="file-label" style="width: 100%">
                                                <input
                                                  id="input_answer_pic_${post['_id']}"
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
                          <!-- Modal Report -->
              <div id="reportModal" class="modal">
                <div class="modal-background"></div>
                <div class="modal-card">
                  <header class="modal-card-head">
                    <p class="modal-card-title">Report Post</p>
                    <button class="delete" aria-label="close" onclick="closeModal()"></button>
                  </header>
                  <section class="modal-card-body">
                    <div class="field">
                      <label class="label" for="issueType">Type of Issue</label>
                      <div class="control">
                        <div class="select">
                          <select id="issueType">
                            <option value="Technical Error" selected>Technical Error</option>
                            <option value="Unclear Question">Unclear Question</option>
                            <option value="Rule Violation">Rule Violation</option>
                            <option value="Irrelevant Content">Irrelevant Content</option>
                            <option value="Discrimination or Harassment">Discrimination or Harassment</option>
                            <option value="Spam">Spam</option>
                            <option value="Inaccurate Information">Inaccurate Information</option>
                            <option value="Repeated Question">Repeated Question</option>
                            <option value="Inappropriateness">Inappropriateness</option>
                            <option value="Other">Other</option>
                          </select>
                        </div>
                      </div>
                    </div>
                    <div class="field">
                      <label class="label" for="issueDescription">Description</label>
                      <div class="control">
                        <textarea class="textarea" id="issueDescription"></textarea>
                      </div>
                    </div>
                  </section>
                  <footer class="modal-card-foot">
                    <button class="button is-primary" onclick="submitReport('${id_post}')">Submit</button>
                    <button class="button" onclick="closeModal()">Cancel</button>
                  </footer>
                </div>
              </div>

        </div>
        
    `;
    $("#discussion").append(html_temp);
  }

  function closeModal() {
    // Hide the modal
    $(".modal").removeClass("is-active");
    
    $("#description").val("");
  }

  function submitReport(id_post) {
    // Get the values from the input fields
    let issueType = $("#issueType").val();
    let description = $("#issueDescription").val();
    
    // Perform validation, e.g., check if the fields are empty
    
    // Create an object to store the report data
    let reportData = {
      id_post:id_post,
      issueType: issueType,
      description: description
    };
    
    // Perform an AJAX request to submit the report data to the server
    $.ajax({
      url: "/submit_report",
      type: "POST",
      data: reportData,
      success: function(response) {
        // Handle the success response from the server
        alert(response['msg'])
        // Close the modal
        closeModal();
      }
    });
  }
  
  function showReportModal(postId) {
    // Dapatkan modal element menggunakan ID
    let modal = $("#reportModal");
    modal.addClass("is-active");
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
        if(answers.length>0 & answers.length<3){
        for (let i = 0; i < 2; i++) {
            let answer = answers[i];
            let time_answer = new Date(answer["date"]);
            let time_before2 = time2str(time_answer);
            let answer_temp =
                `
                <div class="w-100 px-lg-3 p-sm-1">
                <div>
                    <div class="d-flex flex-row mb-4">
                        <a class="image is-48x48" style="width:62px;" href="/user/${answer["username"]}">
                            <img class="is-rounded" style="width:48px;" src="../static/${answer["profile_pic_real"]}"
                                alt="Image">
                        </a>
                        <div class="card d-flex flex-column mx-2 p-3 w-100 is-shadowless" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249);">
                            <p class="m-0 p-0">
                                <strong>${answer["profile_name"]}</strong>                 
                            </p>
                            <p class="m-0 p-0">
                            <small>@${answer["username"]}</small> <small>${time_before2}</small>      
                            </p>
                          
                            <p>${answer['answer']}</p>
                          
                        </div>
                    </div>
                
                </div> 
                `
            $(`#answer-${postID}`).append(answer_temp);

          }
        }
        else if(answers.length>=3){
          for (let i = 0; i < 3; i++) {
              let answer = answers[i];
              let time_answer = new Date(answer["date"]);
              let time_before2 = time2str(time_answer);
              let answer_temp =
                  `
                  <div class="w-100 px-lg-3 p-sm-1">
                  <div>
                      <div class="d-flex flex-row mb-4">
                          <a class="image is-48x48" style="width:62px;" href="/user/${answer["username"]}">
                              <img class="is-rounded" style="width:48px;" src="../static/${answer["profile_pic_real"]}"
                                  alt="Image">
                          </a>
                          <div class="card d-flex flex-column mx-2 p-3 w-100 is-shadowless" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249);">
                              <p class="m-0 p-0">
                                  <strong>${answer["profile_name"]}</strong>                 
                              </p>
                              <p class="m-0 p-0">
                              <small>@${answer["username"]}</small> <small>${time_before2}</small>      
                              </p>
                            
                              <p>${answer['answer']}</p>
                            
                          </div>
                      </div>
                  
                  </div> 
                  `

            $(`#answer-${postID}`).append(answer_temp);
                
            }
          }
      }
    }

  })  
}

  function getAnswer_detail(postID) {
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
                  <div class="w-100 px-lg-3 p-sm-1">
                  <div>
                      <div class="d-flex flex-row mb-4">
                          <a class="image is-48x48" style="width:62px;" href="/user/${answer["username"]}">
                              <img class="is-rounded" style="width:48px;" src="../static/${answer["profile_pic_real"]}"
                                  alt="Image">
                          </a>
                          <div class="card d-flex flex-column mx-2 p-3 w-100 is-shadowless" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249);">
                              <p class="m-0 p-0">
                                  <strong>${answer["profile_name"]}</strong>                 
                              </p>
                              <p class="m-0 p-0">
                              <small>@${answer["username"]}</small> <small>${time_before2}</small>      
                              </p>
                            
                              <p>${answer['answer']}</p>
                            
                          </div>
                      </div>
                  
                  </div> 
                  `

            $('#answer').append(answer_temp);
                
            }
          }
      }
    }

  })  
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