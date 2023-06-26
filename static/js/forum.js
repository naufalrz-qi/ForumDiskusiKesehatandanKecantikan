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
                swal("Success",response["msg"], "success");
                window.location.replace('/')
              }
              else if (response["result"] === "failed") {
                swal("Failed",response["msg"], "error");
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
                swal("Success",response["msg"], "success");
                window.location.replace('/')
              }
            
        }
    })
}


function answer(id_post) {
    let input_answer = $("#textarea-answer-"+id_post).val()
    let file = ''
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
                swal("Success", response["msg"], "success");
                $(`#answer2`).empty()
                $(`#answer-`+id_post).empty()
                $(`#textarea-answer-`+id_post).val('')
                $("#modal-answer").removeClass("is-active")
                $("#modal-answer-"+id_post).removeClass("is-active")
                
                getAnswer(id_post)
                getAnswer_detail(id_post)

              }
            else if(response["result"] === 'failed'){
              swal("Failed",response["msg"], "error");

            }
            
        }
    })
}

function editing_answer(id_post,text,answerID) {
    let input_answer = text
    let file = ''
    let paragraph = input_answer.split("\n")
    let answer = ""
    for(let i = 0; i<paragraph.length; i++){
      answer += paragraph[i]+"<br>";
    }
    let form_data = new FormData();
    let today = new Date().toISOString()
    form_data.append("id_post", id_post);
    form_data.append("id_answer", answerID);
    form_data.append("answer_give", answer);
    form_data.append("file_give", file);
    form_data.append("date_give", today);
    console.log(form_data);
    $.ajax({
        type: "POST",
        url: "/edit_answer",
        data:form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["result"] === "success") {
              swal("Success",response["msg"], "success");

                
              }
            else if(response["result"] === 'failed'){
              swal("Failed",response["msg"], "error");

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
    
            <li><a href="/post_detail/${post['_id']}" class="h6 has-text-link" style="font-size: 14px; ">${post['title']}</a></li>


            
            `;
            $("#must-read").append(html_temp);    
          }
          for (let i = 4; i < 6; i++) {
            let post = posts[i];
            let html_temp2 = `
    
            <li><a href="/post_detail/${post['_id']}" class="h6 has-text-link" style="font-size: 14px; ">${post['title']}</a></li>


            
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

function copy_button(id_post){
  var shareLink = $("#shareLink"+id_post).val();

    // Membuat elemen textarea sementara untuk menyalin teks
    var tempTextarea = $("<textarea>").val(shareLink).css("position", "fixed").appendTo("body").select();

    // Menyalin teks ke clipboard
    document.execCommand("copy");

    // Menghapus elemen textarea sementara
    tempTextarea.remove();

    // Menampilkan pesan sukses
    swal("Link copied to clipboard!");
}

  function btn_share(id_post){
      let currentURL = window.location.href;
      let url = currentURL.split("/")
      let modifiedUrl = url.slice(0, 3).join("/");
      $('#modal-share-'+id_post).addClass('is-active');

      $("#shareLink"+id_post).val(modifiedUrl + '/post_detail/'+ id_post);
  }

  function showPost(post, time_post) {  
    let time_before = time2str(time_post);
    let class_up = post['up_by_me'] ? "is-primary": "text-body-tertiary"
    const username = $('script[data-username]').data('username');
    let id_post = post['_id']
    let status_verified = '';
            if(post["status"] == 'verified'){
              status_verified = `
              <span class="button is-primary is-static text-white" style="font-size:12px; padding: 3px; border: 0px; height: 18px; background-color: #00d1b2; border-color: #00d1b2;">Expert</span>
             `
            }
    let cek_admin = username === 'admin'
    let editPostHtml = '';
    if (post['username'] === username) {
    editPostHtml = `<a class="dropdown-item" href="/edit_post/${post['_id']}"><span>Edit post</span></a>
                    <a class="dropdown-item" href="#" onclick="confirmDelete('${post['_id']}')"><span>Delete Post</span></a>
    `;
    }else if(cek_admin){
      editPostHtml = `<a class="dropdown-item" href="#" onclick="confirmDelete('${post['_id']}')"><span>Delete Post</span></a>`
    };

    let html_temp = `
      
        <div class="card w-100 my-3" style="border-radius: 30px;">
            <div class="card-body p-5">
            <div class="d-flex flex-row mb-5">
            <div class="col-11">
              <a id="topics_${post['_id']}" class="btn btn-success p-1 m-0" href="/topic/${post['topic']}" style="font-size:10px; width: fit-content;">${post['topic']}</a>
            </div>
            <a class="bi bi-three-dots-vertical col-1 d-flex justify-content-end" onclick="$('#post_drop_${post['_id']}').toggleClass('is-active')" style="font-size: 18px; color: inherit;"></a>
            <div class="dropdown is-right" id="post_drop_${post['_id']}">
              <div class="dropdown-menu">
                <div class="dropdown-content">
                  ${editPostHtml}
                  <a class="dropdown-item" href="/post_detail/${post['_id']}"><span>View Detail</span></a>
                  <a class="dropdown-item" href="#" onclick="showReportModal()"><span>Report</span></a>
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
                            ${status_verified}              
                        </p>
                        <p class="m-0 p-0">
                        <small>@${post["username"]}</small> <small>${time_before}</small>      
                        </p>   
                    </div>
                </div>
                
                <div class="mt-5">
                  <a href="/post_detail/${post['_id']}" style="color: currentColor;">
                    <p>${post['question']}</p>
                  </a>
                      
                </div>
                

            </div>
            <div class="d-flex justify-content-center" onclick="$('#img_post_${post['_id']}').toggleClass('w-100')" style="height: 300px;">
                <img id="img_post_${post['_id']}" src="../static/${post['post_pic_real']}" alt="" class="w-100" style="object-fit: cover;">
            </div>

            
            <hr class="separator m-0 my-3 mx-5 p-0 px-5">
            <div class="d-flex justify-content-end px-5">
              <a id="up_${post['_id']}" onclick="toggle_up('${post["_id"]}', 'up')" class="bi bi-arrow-up has-text-weight-bold me-3 ${class_up}" style="font-size:16px;">
                <span class="up-num" style="font-size:16px;">${num2str(post["count_up"])}</span>
              </a>
              <a id="answer_count_${post['_id']}" class="bi bi-chat-left has-text-weight-bold text-body-tertiary me-3" style="font-size:16px;"></a>
              <a id="shareButton${id_post}" onclick="btn_share('${id_post}')" class="bi bi-share has-text-weight-bold text-body-tertiary" data-toggle="modal" data-target="#shareModal" style="font-size:16px;">
                Share
              </a>

              <!-- Modal -->
              <div class="modal" id="modal-share-${post['_id']}">
                  <div class="modal-background" onclick='$("#modal-share-${post['_id']}").removeClass("is-active")'></div>
                  <div class="modal-content">
            
                          <article class="media">
                              <div class="media-content p-5">
                                  <div class="field">
                                  <input id="shareLink${post['_id']}" class="form-control" type="text" readonly>
                                  </div>
                                  
                                  <nav class="level is-mobile">
                                      <div class="level-right">
                                          <div class="level-item">
                                              <a class="button is-primary" id="copyButton${post['_id']}" onclick="copy_button('${id_post}')">Copy</a>
                                          </div>
                                          <div class="level-item">
                                              <a class="button is-primary is-outlined"
                                                onclick='$("#modal-share-${post['_id']}").removeClass("is-active")'>Cancel</a>
                                          </div>
                                      </div>
                                  </nav>
                              </div>
                          </article>
                      
                  </div>
                  <button class="modal-close is-large" aria-label="close"
                          onclick='$("#modal-share-${post['_id']}").removeClass("is-active")'></button>
              </div>
   

            </div>
            <hr class="separator m-0 my-3 mx-5 p-0 px-5">
            <section id="answer" class="p-3">
              <p class="h6 has-text-weight-bold px-lg-3"><a class="text-body-secondary" href="/post_detail/${post['_id']}" >See another answer</a></p>
              <article class="media" style="margin-bottom:0px;">
                  <div class="media-content">
                      <div class="field px-lg-3">
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
    let topicsElement = $("#topics_"+id_post);

    // Mendapatkan teks awal dari elemen
    let originalText = topicsElement.text();

    // Mengganti tanda minus dengan spasi
    let modifiedText = originalText.replace(/-/g, " ");

    // Mengubah teks menjadi huruf kecil di awal setiap kata
    if (modifiedText.includes(" ")) {
      modifiedText = modifiedText.replace(/\b\w/g, function(match) {
        return match.toUpperCase();
      });
    } else {
      modifiedText = modifiedText.charAt(0).toUpperCase() + modifiedText.slice(1);
    }

    // Mengatur teks yang telah dimodifikasi ke elemen
    topicsElement.text(modifiedText);
  }

  function num2str(count_number) {
    console.log(count_number)
    if(count_number!='' || count_number!=undefined){
      let count = parseInt(count_number)
    if (count > 10000) {
        return parseInt(count / 1000) + "k"
    }
    if (count > 500) {
        return parseInt(count / 100) / 10 + "k"
    }
    if (count == 0) {
        return 0
    }
    return count
    }else{
      let count = 0
      return count
    }
    
}

function get_topics(value) {
  $.ajax({
    type: "GET",
    url: "/get_topics",
    success: function(response) {
      if (response["result"] === "success") {
        let topics = response["topics"];
        let selectElement = $("#select_topic");

        for (let category in topics) {
          let categoryGroup = $("<optgroup>").attr("label", category);

          topics[category].forEach(function(topic) {
            let topicText = topic.topic;
            let option = $("<option>").val(topic.index).text(topicText);
            categoryGroup.append(option);
          });

          selectElement.append(categoryGroup);
        }
        if(topics.length === topics.length){
          $('#select_topic').val(value)
        }
        
        
      }
    }
  });
}


function get_posts_by_topic(topic) {

  $("#discussion").empty();   
  $.ajax({
    type: "POST",
    url: '/topic/'+topic,
    data: {},
    success: function (response) {
      if (response["result"] === "success") {
        let posts = response["posts"];
        if(posts.length>0){
          for (let i = 0; i < posts.length; i++) {
            let post = posts[i];
            let id= post['_id']
            let time_post = new Date(post["date"]);
            
            showPost(post, time_post)
            getAnswer(id)
          }
        }else{
          showAlert('There are no posts related to this topic');
        }
      }
    },
  });
}

  function toggle_up(post_id, type) {
    console.log(post_id, type);
    let $a_like = $(`#up_${post_id}`);
    if ($a_like.hasClass("is-primary")) {
      $.ajax({
        type: "POST",
        url: "/update_like",
        data: {
          post_id_give: post_id,
          type_give: type,
          action_give: "unlike",
        },
        success: function (response) {
          console.log("unlike");
          $a_like.addClass("text-body-tertiary").removeClass("is-primary");
          $a_like.find("span.up-num").text(num2str(response["count"]));
        },
      });
    } else {
      $.ajax({
        type: "POST",
        url: "/update_like",
        data: {
          post_id_give: post_id,
          type_give: type,
          action_give: "like",
        },
        success: function (response) {
          console.log("like");
          $a_like.addClass("is-primary").removeClass("text-body-tertiary");
          $a_like.find("span.up-num").text(num2str(response["count"]));
        },
      });
    }
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
        swal("Success",response["msg"], "success");
        // Close the modal
        closeModal();
      }
    });
  }
  
  function showReportModal() {
    // Dapatkan modal element menggunakan ID
    let modal = $("#reportModal");
    modal.addClass("is-active");
  }
  function showReportModalAnswer() {
    // Dapatkan modal element menggunakan ID
    let modal = $("#reportModalAnswer");
    modal.addClass("is-active");
  }
  function showReportModalReply() {
    // Dapatkan modal element menggunakan ID
    let modal = $("#reportModalReply");
    modal.addClass("is-active");
  }

  function getAnswer(postID) {
    
    $.ajax({
    type:"POST",
    url:'/get_answers',
    data:{'id_post':postID},
    success:function(response){
      const username = $('script[data-username]').data('username');
     
      
      if (response["result"] === "success") {
        let answers = response["answers"];
        console.log(answers)
        let reply_counting = 0
        let reply_counting2 = 0
        if(answers.length>0 & answers.length<3){
        for (let i = 0; i < 2; i++) {
            let answer = answers[i];
            let dropdownToggle = $('#answer_drop_toggle_'+answer["_id"]);
            dropdownToggle.dropdown();
            let count_replies = num2str(answer["count_replies"])
            console.log(count_replies)
            let time_answer = new Date(answer["date"]);
            let time_before2 = time2str(time_answer);
            console.log
            console.log(answer['username'],username)
            let status_verified = '';
            if(answer["status"] == 'verified'){
              status_verified = `
              <span class="button is-primary is-static text-white" style="font-size:12px; padding: 3px; border: 0px; height: 18px; background-color: #00d1b2; border-color: #00d1b2;">Expert</span>
             `
            }
            let editAnswerHtml = '';
            let cek_admin = username === 'admin'
            if (answer['username'] === username ) {
              editAnswerHtml = `<a class="dropdown-item" onclick="editAnswer('${answer['_id']}','${postID}')"><span>Edit Answer</span></a>
                              <a class="dropdown-item" onclick="confirmDeleteAnswer('${answer['_id']}')"><span>Delete Answer</span></a>
              `;
              }else if(cek_admin){
                editAnswerHtml = `<a class="dropdown-item" onclick="confirmDeleteAnswer('${answer['_id']}')"><span>Delete Answer</span></a>`
              }
            let answer_temp =
                `
          
                <div id="answer_${answer['_id']}" class="w-100 px-lg-3 p-sm-1">
                <div>
                    <div class="d-flex flex-row mb-4">
                        <a class="image is-48x48" style="width:62px;" href="/user/${answer["username"]}">
                            <img class="is-rounded" style="width:48px;" src="../static/${answer["profile_pic_real"]}"
                                alt="Image">
                        </a>
                      <div class="d-flex flex-column mx-2" style="width:fit-content;">
                        <div class="card d-flex flex-column p-3 w-100 is-shadowless" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249);">
                              <p class="m-0 p-0">
                                  <strong>${answer["profile_name"]}</strong>   
                                  ${status_verified}             
                              </p>
                              <p class="m-0 p-0">
                              <small>@${answer["username"]}</small> <small>${time_before2}</small>      
                              </p>
                            
                              <p id="${answer['_id']}">${answer['answer']}</p>

                              

                        </div>
                        <a class="reply-link mx-3"  id="reply_toggle_${answer["_id"]}" onclick="toggleReplyContainer('${answer["_id"]}')">Reply(${count_replies})</a>
                            <div id="reply_${answer["_id"]}" class="reply-container" style="display: none;">
                              
                              <div class="d-flex flex-row card p-3 is-shadowless" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249); width: fit-content;">
                              <textarea type="text" id="input-reply-${answer["_id"]}" class="reply-input" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249);" data-answer-id="${answer["_id"]}" placeholder="Type your reply..."></textarea>

                                <button onclick="sendReply('${answer["_id"]}','${postID}','${answer['username']}')" class="button is-primary is-outlined reply-submit" style="border: none !important;" data-answer-id="${answer["_id"]}"><span class="bi bi-send-fill fs-5"></span></button>                            
                              </div>
                            </div>
                        </div>
                        
                        <div class="d-flex justify-content-center align-content-center align-items-center" style="height: 87px;">
                          <a class="bi bi-three-dots " id="answer_drop_toggle_${answer["_id"]}" aria-controls="answer_drop_${answer["_id"]}" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 18px; color: inherit; "></a>
                          <div class="dropdown-menu" id="answer_drop_${answer["_id"]}" aria-labelledby="answer_drop_toggle_${answer["_id"]}">
                            <div class="dropdown-content">
                              ${editAnswerHtml}
                              <a class="dropdown-item" onclick="showReportModalAnswer()"><span>Report</span></a>
                            </div>
                          </div>
                        </div>
                       
                    </div>
                
                </div>
                <!-- Modal Report -->
                <div id="reportModalAnswer" class="modal">
                  <div class="modal-background"></div>
                  <div class="modal-card">
                    <header class="modal-card-head">
                      <p class="modal-card-title">Report Answer</p>
                      <button class="delete" aria-label="close" onclick="closeModal()"></button>
                    </header>
                    <section class="modal-card-body">
                      <div class="field">
                        <label class="label" for="issueTypeAnswer">Type of Issue</label>
                        <div class="control">
                          <div class="select">
                            <select id="issueTypeAnswer">
                              <option value="Technical Error" selected>Technical Error</option>
                              <option value="Unclear Answer">Unclear Answer</option>
                              <option value="Rule Violation">Rule Violation</option>
                              <option value="Irrelevant Content">Irrelevant Content</option>
                              <option value="Discrimination or Harassment">Discrimination or Harassment</option>
                              <option value="Spam">Spam</option>
                              <option value="Inaccurate Information">Inaccurate Information</option>
                              <option value="Repeated Answer">Repeated Answer</option>
                              <option value="Inappropriateness">Inappropriateness</option>
                              <option value="Other">Other</option>
                            </select>
                          </div>
                        </div>
                      </div>
                      <div class="field">
                        <label class="label" for="issueDescriptionAnswer">Description</label>
                        <div class="control">
                          <textarea class="textarea" id="issueDescriptionAnswer"></textarea>
                        </div>
                      </div>
                    </section>
                    <footer class="modal-card-foot">
                      <button class="button is-primary" onclick="submitReportAnswer('${postID}','${answer['_id']}')">Submit</button>
                      <button class="button" onclick="closeModal()">Cancel</button>
                    </footer>
                  </div>
                </div>
                 
                `
            $(`#answer-${postID}`).append(answer_temp);
            reply_counting += parseInt(count_replies)

          }
          let count = answers.length+reply_counting
          let answer_count = `<span style="font-size: 16px;"> ${count}</span>`
          $(`#answer_count_${postID}`).empty()
          $(`#answer_count_${postID}`).append(answer_count);
        }
        else if(answers.length>=3){
          for (let i = 0; i < 3; i++) {
              let answer = answers[i];
              let dropdownToggle = $('#answer_drop_toggle_'+answer["_id"]);
              dropdownToggle.dropdown();
              let count_replies = num2str(answer["count_replies"])
              let time_answer = new Date(answer["date"]);
              let time_before2 = time2str(time_answer);
              console.log(answer['username'],username)
              let status_verified = '';
            if(answer["status"] == 'verified'){
              status_verified = `
              <span class="button is-primary is-static text-white" style="font-size:12px; padding: 3px; border: 0px; height: 18px; background-color: #00d1b2; border-color: #00d1b2;">Expert</span>
             `
            }
              let editAnswerHtml = '';
              let cek_admin = username === 'admin'
              if (answer['username'] === username) {
                editAnswerHtml = `<a class="dropdown-item" onclick="editAnswer('${answer['_id']}','${postID}')"><span>Edit Answer</span></a>
                                <a class="dropdown-item" onclick="confirmDeleteAnswer('${answer['_id']}')"><span>Delete Answer</span></a>
                `;
                }else if( cek_admin){
                  editAnswerHtml = `<a class="dropdown-item" onclick="confirmDeleteAnswer('${answer['_id']}')"><span>Delete Answer</span></a>`
                }
              let answer_temp =
              `
          
              <div id="answer_${answer['_id']}" class="w-100 px-lg-3 p-sm-1">
              <div>
                  <div class="d-flex flex-row mb-4">
                      <a class="image is-48x48" style="width:62px;" href="/user/${answer["username"]}">
                          <img class="is-rounded" style="width:48px;" src="../static/${answer["profile_pic_real"]}"
                              alt="Image">
                      </a>
                    <div class="d-flex flex-column mx-2" style="width:fit-content;">
                      <div class="card d-flex flex-column p-3 w-100 is-shadowless" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249);">
                            <p class="m-0 p-0">
                                <strong>${answer["profile_name"]}</strong>
                                ${status_verified}                 
                            </p>
                            <p class="m-0 p-0">
                            <small>@${answer["username"]}</small> <small>${time_before2}</small>      
                            </p>
                          
                            <p id="${answer['_id']}">${answer['answer']}</p>

                            

                      </div>
                      <a class="reply-link mx-3"  id="reply_toggle_${answer["_id"]}" onclick="toggleReplyContainer('${answer["_id"]}')">Reply(${count_replies})</a>
                          <div id="reply_${answer["_id"]}" class="reply-container" style="display: none;">
                            
                            <div class="d-flex flex-row card p-3 is-shadowless" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249); width: fit-content;">
                            <textarea type="text" id="input-reply-${answer["_id"]}" class="reply-input" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249);" data-answer-id="${answer["_id"]}" placeholder="Type your reply..."></textarea>

                              <button onclick="sendReply('${answer["_id"]}','${postID}','${answer['username']}')" class="button is-primary is-outlined reply-submit" style="border: none !important;" data-answer-id="${answer["_id"]}"><span class="bi bi-send-fill fs-5"></span></button>                            
                            </div>
                          </div>
                      </div>
                      <div class="d-flex justify-content-center align-content-center align-items-center" style="height: 87px;">
                        <a class="bi bi-three-dots " id="answer_drop_toggle_${answer["_id"]}" aria-controls="answer_drop_${answer["_id"]}" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 18px; color: inherit; "></a>
                        <div class="dropdown-menu" id="answer_drop_${answer["_id"]}" aria-labelledby="answer_drop_toggle_${answer["_id"]}">
                          <div class="dropdown-content">
                            ${editAnswerHtml}
                            <a class="dropdown-item" onclick="showReportModalAnswer()"><span>Report</span></a>
                          </div>
                        </div>
                      </div>
                     



                      





                  </div>
              
              </div>
              <!-- Modal Report -->
              <div id="reportModalAnswer" class="modal">
                <div class="modal-background"></div>
                <div class="modal-card">
                  <header class="modal-card-head">
                    <p class="modal-card-title">Report Answer</p>
                    <button class="delete" aria-label="close" onclick="closeModal()"></button>
                  </header>
                  <section class="modal-card-body">
                    <div class="field">
                      <label class="label" for="issueTypeAnswer">Type of Issue</label>
                      <div class="control">
                        <div class="select">
                          <select id="issueTypeAnswer">
                            <option value="Technical Error" selected>Technical Error</option>
                            <option value="Unclear Answer">Unclear Answer</option>
                            <option value="Rule Violation">Rule Violation</option>
                            <option value="Irrelevant Content">Irrelevant Content</option>
                            <option value="Discrimination or Harassment">Discrimination or Harassment</option>
                            <option value="Spam">Spam</option>
                            <option value="Inaccurate Information">Inaccurate Information</option>
                            <option value="Repeated Answer">Repeated Answer</option>
                            <option value="Inappropriateness">Inappropriateness</option>
                            <option value="Other">Other</option>
                          </select>
                        </div>
                      </div>
                    </div>
                    <div class="field">
                      <label class="label" for="issueDescriptionAnswer">Description</label>
                      <div class="control">
                        <textarea class="textarea" id="issueDescriptionAnswer"></textarea>
                      </div>
                    </div>
                  </section>
                  <footer class="modal-card-foot">
                    <button class="button is-primary" onclick="submitReportAnswer('${postID}','${answer['_id']}')">Submit</button>
                    <button class="button" onclick="closeModal()">Cancel</button>
                  </footer>
                </div>
              </div>
              `

            $(`#answer-${postID}`).append(answer_temp);
            reply_counting2 += parseInt(count_replies)
                
            }
          let count = answers.length+reply_counting2
          let answer_count = `<span style="font-size: 16px;"> ${count}</span>`
          $(`#answer_count_${postID}`).empty()
          $(`#answer_count_${postID}`).append(answer_count);
          }
      }
    }

  })  
}

function toggleReplyContainer(answerID) {
  $(`#reply_${answerID} input.reply-input`).val('');
  $(`#reply_${answerID}`).toggle();
}

  function getReplies_detail(answerID,userReplyTo) {
    $('#replies_'+answerID).empty();
    $.ajax({
    type:"POST",
    url:'/get_replies',
    data:{'id_answer':answerID},
    success:function(response){
      if (response["result"] === "success") {
        let replies = response["replies"];
        let count_replies = replies['count_replies']
        const username = $('script[data-username]').data('username');
        console.log(response['replies'])
        if(replies.length>0){
          for (let i = 0; i < replies.length; i++) {
              let reply = replies[i];
              let time_reply = new Date(reply["date"]);
              let time_before2 = time2str(time_reply);
              let status_verified = '';
            if(reply["status"] == 'verified'){
              status_verified = `
              <span class="button is-primary is-static text-white" style="font-size:12px; padding: 3px; border: 0px; height: 18px; background-color: #00d1b2; border-color: #00d1b2;">Expert</span>
             `
            }
              let cek_admin = username === 'admin'
              let editReplyHtml = ''
              if (reply['username'] === username) {
                editReplyHtml = `<a class="dropdown-item" onclick="editReply('${reply['_id']}','${answerID}')"><span>Edit Reply</span></a>
                                <a class="dropdown-item" onclick="confirmDeleteReply('${reply['_id']}')"><span>Delete Reply</span></a>
                `;
                }else if(cek_admin){
                  editReplyHtml = `<a class="dropdown-item" onclick="confirmDeleteReply('${reply['_id']}')"><span>Delete Reply</span></a>
                  `;
                }
              let reply_temp =
                  `
                  
                      <div id="reply_${reply['_id']}" class="d-flex flex-row mt-4 mb-4">
                          <a class="image is-48x48" style="width:62px;" href="/user/${reply["username"]}">
                              <img class="is-rounded" style="width:48px;" src="../static/${reply["profile_pic_real"]}"
                                  alt="Image">
                          </a>
                          <div class="card d-flex flex-column mx-2 p-3 w-100 is-shadowless" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249);">
                              <p class="m-0 p-0">
                                  <strong>${reply["profile_name"]}</strong>
                                   ${status_verified}
                                  <small>reply to @${userReplyTo}<small>                
                              </p>
                              <p class="m-0 p-0">
                              <small>@${reply["username"]}</small> <small>${time_before2}</small>      
                              </p>
                            
                              <p id="${reply['_id']}">${reply['reply']}</p>

                          </div>
                          <div class="d-flex justify-content-center align-content-center align-items-center" style="height: 87px;">
                              <a class="bi bi-three-dots " id="reply_drop_toggle_${reply["_id"]}" aria-controls="reply_drop_${reply["_id"]}" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 18px; color: inherit; "></a>
                              <div class="dropdown-menu" id="reply_drop_${reply["_id"]}" aria-labelledby="reply_drop_toggle_${reply["_id"]}">
                                <div class="dropdown-content">
                                  ${editReplyHtml}
                            <a class="dropdown-item" onclick="showReportModalReply()"><span>Report</span></a>
                          </div>
                        </div>
                      </div>
                      </div>
                      <!-- Modal Report -->
                      <div id="reportModalReply" class="modal">
                        <div class="modal-background"></div>
                        <div class="modal-card">
                          <header class="modal-card-head">
                            <p class="modal-card-title">Report reply</p>
                            <button class="delete" aria-label="close" onclick="closeModal()"></button>
                          </header>
                          <section class="modal-card-body">
                            <div class="field">
                              <label class="label" for="issueTypeReply">Type of Issue</label>
                              <div class="control">
                                <div class="select">
                                  <select id="issueTypeReply">
                                    <option value="Technical Error" selected>Technical Error</option>
                                    <option value="Unclear Reply">Unclear Reply</option>
                                    <option value="Rule Violation">Rule Violation</option>
                                    <option value="Irrelevant Content">Irrelevant Content</option>
                                    <option value="Discrimination or Harassment">Discrimination or Harassment</option>
                                    <option value="Spam">Spam</option>
                                    <option value="Inaccurate Information">Inaccurate Information</option>
                                    <option value="Repeated Reply">Repeated Reply</option>
                                    <option value="Inappropriateness">Inappropriateness</option>
                                    <option value="Other">Other</option>
                                  </select>
                                </div>
                              </div>
                            </div>
                            <div class="field">
                              <label class="label" for="issueDescriptionReply">Description</label>
                              <div class="control">
                                <textarea class="textarea" id="issueDescriptionReply"></textarea>
                              </div>
                            </div>
                          </section>
                          <footer class="modal-card-foot">
                            <button class="button is-primary" onclick="submitReportReply('${answerID}','${reply['_id']}')">Submit</button>
                            <button class="button" onclick="closeModal()">Cancel</button>
                          </footer>
                        </div>
                      </div>
                  `

            
            $('#replies_'+answerID).append(reply_temp);
                
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
      const username = $('script[data-username]').data('username');
      if (response["result"] === "success") {
        let answers = response["answers"];
        
        let reply_counting = 0
        console.log(response['answers'])
       
        if(answers.length>0){
          for (let i = 0; i < answers.length; i++) {
              let answer = answers[i];
              let time_answer = new Date(answer["date"]);
              let count_replies = num2str(answer["count_replies"])
              let status_verified = '';
            if(answer["status"] == 'verified'){
              status_verified = `
              <span class="button is-primary is-static text-white" style="font-size:12px; padding: 3px; border: 0px; height: 18px; background-color: #00d1b2; border-color: #00d1b2;">Expert</span>
             `
            }
              let editAnswerHtml = '';
              let cek_admin = username === 'admin'
              if (answer['username'] === username) {
                editAnswerHtml = `<a class="dropdown-item" onclick="editAnswer('${answer['_id']}','${postID}')"><span>Edit Answer</span></a>
                                <a class="dropdown-item" onclick="confirmDeleteAnswer('${answer['_id']}')"><span>Delete Answer</span></a>
                `;
                }else if( cek_admin){
                  editAnswerHtml = `<a class="dropdown-item" onclick="confirmDeleteAnswer('${answer['_id']}')"><span>Delete Answer</span></a>`
                }
              let time_before2 = time2str(time_answer);
              let answer_temp =
                  `
                  <div id="answer_${answer['_id']}" class="w-100 px-lg-3 p-sm-1">
              <div>
                  <div class="d-flex flex-row mb-4">
                      <a class="image is-48x48" style="width:62px;" href="/user/${answer["username"]}">
                          <img class="is-rounded" style="width:48px;" src="../static/${answer["profile_pic_real"]}"
                              alt="Image">
                      </a>
                    <div class="d-flex flex-column mx-2" style="width:fit-content;">
                      <div class="card d-flex flex-column p-3 w-100 is-shadowless" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249);">
                            <p class="m-0 p-0">
                                <strong>${answer["profile_name"]}</strong>    
                                ${status_verified}             
                            </p>
                            <p class="m-0 p-0">
                            <small>@${answer["username"]}</small> <small>${time_before2}</small>      
                            </p>
                          
                            <p id="${answer['_id']}">${answer['answer']}</p>

                            

                      </div>
                      <a class="reply-link mx-3"  id="reply_toggle_${answer["_id"]}" onclick="toggleReplyContainer('${answer["_id"]}')">Reply(${count_replies})</a>
                          <div id="reply_${answer["_id"]}" class="reply-container" style="display: none;">
                            
                            <div class="d-flex flex-row card p-3 is-shadowless" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249); width: fit-content;">
                              <textarea type="text" id="input-reply-${answer["_id"]}" class="reply-input" style="border: 0px; border-radius: 20px; background-color: rgb(241, 245, 249);" data-answer-id="${answer["_id"]}" placeholder="Type your reply..."></textarea>
                              <button onclick="sendReply('${answer["_id"]}','${postID}','${answer['username']}')" class="button is-primary is-outlined reply-submit" style="border: none !important;" data-answer-id="${answer["_id"]}"><span class="bi bi-send-fill fs-5"></span></button>                            
                            </div>

                            <div id=replies_${answer["_id"]}>
                            </div>
                          </div>
                      </div>

                      <div class="d-flex justify-content-center align-content-center align-items-center" style="height: 87px;">
                        <a class="bi bi-three-dots " id="answer_drop_toggle_${answer["_id"]}" aria-controls="answer_drop_${answer["_id"]}" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 18px; color: inherit; "></a>
                        <div class="dropdown-menu" id="answer_drop_${answer["_id"]}" aria-labelledby="answer_drop_toggle_${answer["_id"]}">
                          <div class="dropdown-content">
                            ${editAnswerHtml}
                            <a class="dropdown-item" onclick="showReportModalAnswer()"><span>Report</span></a>
                          </div>
                        </div>
                      </div>
                     



                      





                  </div>
              
              </div>
              <!-- Modal Report -->
              <div id="reportModalAnswer" class="modal">
                <div class="modal-background"></div>
                <div class="modal-card">
                  <header class="modal-card-head">
                    <p class="modal-card-title">Report Answer</p>
                    <button class="delete" aria-label="close" onclick="closeModal()"></button>
                  </header>
                  <section class="modal-card-body">
                    <div class="field">
                      <label class="label" for="issueTypeAnswer">Type of Issue</label>
                      <div class="control">
                        <div class="select">
                          <select id="issueTypeAnswer">
                            <option value="Technical Error" selected>Technical Error</option>
                            <option value="Unclear Answer">Unclear Answer</option>
                            <option value="Rule Violation">Rule Violation</option>
                            <option value="Irrelevant Content">Irrelevant Content</option>
                            <option value="Discrimination or Harassment">Discrimination or Harassment</option>
                            <option value="Spam">Spam</option>
                            <option value="Inaccurate Information">Inaccurate Information</option>
                            <option value="Repeated Answer">Repeated Answer</option>
                            <option value="Inappropriateness">Inappropriateness</option>
                            <option value="Other">Other</option>
                          </select>
                        </div>
                      </div>
                    </div>
                    <div class="field">
                      <label class="label" for="issueDescriptionAnswer">Description</label>
                      <div class="control">
                        <textarea class="textarea" id="issueDescriptionAnswer"></textarea>
                      </div>
                    </div>
                  </section>
                  <footer class="modal-card-foot">
                    <button class="button is-primary" onclick="submitReportAnswer('${postID}','${answer['_id']}')">Submit</button>
                    <button class="button" onclick="closeModal()">Cancel</button>
                  </footer>
                </div>
              </div>
                  `

            getReplies_detail(answer["_id"],answer["username"])
                  
            $(`#answer2`).append(answer_temp);
            reply_counting += parseInt(count_replies)
                
            }
          let count = answers.length+reply_counting
          let answer_count = `<span style="font-size: 16px;"> ${count}</span>`
          $(`#answer_count_${postID}`).empty()
          $(`#answer_count_${postID}`).append(answer_count);
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

function editAnswer(answerId,postID) {
  let answerElement = $("#" + answerId);
  let originalContent = answerElement.text();

  let editInput = $("<textarea>").attr({
    class: "edit-answer",
  }).text(originalContent.replace(/<br>/g, '\n'));

  answerElement.empty().append(editInput);

  editInput.focus();

  editInput.keydown(function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      let editedContent = editInput.val();

      editing_answer(postID,editedContent,answerId);
      let paragraph = editedContent.split("\n")
      let answer = ""
      for(let i = 0; i<paragraph.length; i++){
        answer += paragraph[i]+"<br>";
      }
      answerElement.empty().html(answer);
    }
  });
}

function confirmDeleteAnswer(answerId) {
  let confirmation = confirm("Apakah Anda yakin ingin menghapus jawaban ini?");

  if (confirmation) {
    $("#answer_" + answerId).remove();
    $.ajax({
      type: "POST",
      url: "/delete_answer",
      data:{'id_answer':answerId},
      success: function (response) {
          if (response["result"] === "success") {
            swal("Success",response["msg"], "success");
            }
          else if(response["result"] === 'failed'){
            swal("Failed",response["msg"], "error");

          }
          
      }
  })
    
  }
}


function submitReportAnswer(id_post,answerID) {
  // Get the values from the input fields
  let issueType = $("#issueTypeAnswer").val();
  let description = $("#issueDescriptionAnswer").val();
  
  // Perform validation, e.g., check if the fields are empty
  
  // Create an object to store the report data
  let reportData = {
    id_post:id_post,
    id_answer:answerID,
    issueType: issueType,
    description: description
  };
  
  // Perform an AJAX request to submit the report data to the server
  $.ajax({
    url: "/submit_report_answer",
    type: "POST",
    data: reportData,
    success: function(response) {
      // Handle the success response from the server
      swal("Success",response["msg"], "success");

      // Close the modal
      closeModal();
    }
  });
}

function editReply(replyID,answerID) {
  let replyElement = $("#" + replyID);
  let originalContent = replyElement.text();

  let editInput = $("<textarea>").attr({
    class: "edit-answer",
  }).text(originalContent.replace(/<br>/g, '\n'));

  replyElement.empty().append(editInput);

  editInput.focus();

  editInput.keydown(function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      let editedContent = editInput.val();

      editing_reply(answerID,editedContent,replyID);
      let paragraph = editedContent.split("\n")
      let reply = ""
      for(let i = 0; i<paragraph.length; i++){
        reply += paragraph[i]+"<br>";
      }
      replyElement.empty().html(reply);
    }
  });
}

function confirmDeleteReply(replyId) {
  let confirmation = confirm("Apakah Anda yakin ingin menghapus jawaban ini?");

  if (confirmation) {
    $("#reply_" + replyId).remove();
    $.ajax({
      type: "POST",
      url: "/delete_reply",
      data:{'id_reply':replyId},
      success: function (response) {
          if (response["result"] === "success") {
            swal("Success",response["msg"], "success");

            }
          else if(response["result"] === 'failed'){
            swal("Failed",response["msg"], "error");

          }
          
      }
  })
    
  }
}


function submitReportReply(answerID,replyID) {
  // Get the values from the input fields
  let issueType = $("#issueTypeReply").val();
  let description = $("#issueDescriptionReply").val();
  
  // Perform validation, e.g., check if the fields are empty
  
  // Create an object to store the report data
  let reportData = {
    id_answer:answerID,
    id_reply:replyID,
    issueType: issueType,
    description: description
  };
  
  // Perform an AJAX request to submit the report data to the server
  $.ajax({
    url: "/submit_report_reply",
    type: "POST",
    data: reportData,
    success: function(response) {
      // Handle the success response from the server
      swal("Success",response["msg"], "success");

      // Close the modal
      closeModal();
    }
  });
}

function editing_reply(answerID,text,replyID) {
  let input_reply = text
  let paragraph = input_reply.split("\n")
  let reply = ""
  for(let i = 0; i<paragraph.length; i++){
    reply += paragraph[i]+"<br>";
  }
  let form_data = new FormData();
  let today = new Date().toISOString()
  form_data.append("id_answer", answerID);
  form_data.append("id_reply", replyID);
  form_data.append("reply_give", reply);
  form_data.append("date_give", today);
  console.log(form_data);
  $.ajax({
      type: "POST",
      url: "/edit_reply",
      data:form_data,
      cache: false,
      contentType: false,
      processData: false,
      success: function (response) {
          if (response["result"] === "success") {
            swal("Success",response["msg"], "success");
 
            }
          else if(response["result"] === 'failed'){
            swal("Failed",response["msg"], "error");

          }
          
      }
  })
}

function sendReply(answerId, postID, userReplyTo) {
  
  let replyText = $('#input-reply-'+answerId).val();
  let paragraph = replyText.split("\n")
  let reply = ""
  for(let i = 0; i<paragraph.length; i++){
    reply += paragraph[i]+"<br>";
  }
  let date = new Date().toISOString()

  $.ajax({
    type: "POST",
    url: "/submit_reply",
    data: {
      post_id: postID,
      answer_id: answerId,
      reply: reply,
      date:date
    },
    success: function(response) {
      if (response.result === "success") {
        swal("Success",response["msg"], "success");
        $(`#reply_toggle_`+answerId).text('reply('+num2str(response["count_replies"])+')');
        $('#input-reply-'+answerId).val('')
        getReplies_detail(answerId,userReplyTo)
      }
    },
  });
}