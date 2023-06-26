
function getNotifications() {
  $('#notification-content').empty();
  $('#notification-content-mobile').empty();
    $.ajax({
    type:"GET",
    url:'/get_notifications',
    success:function(response){
      if (response["result"] === "success") {
        let notifications = response["notifications"];
        let count = num2str(response['count'])
        if(count>0){
          $('#notif_count').text(count);
          $('#notif_countMobile').text(count);
        }else{
          $('#notif_count').text('');
          $('#notif_countMobile').text('');
        }

       
        if (notifications.length > 0){
          $('#notification-content').empty();
          $('#notification-content-mobile').empty();
          
          for (let i = 0; i < notifications.length; i++) {
          let notification = notifications[i];
          let time_notif = new Date(notification['date'])
          console.log(time_notif)
          let times = time2str(time_notif)
          if(notification['status']!='read'){
            let temp_html = `
            <a href="${notification['link']}" class="card-body my-1" style="border-radius:20px; background-color:white;">
              <small>${times}</small>   
              <p><span><strong>From @${notification['by_user']}:</strong></span> ${notification['message']}</p>
          
            </a>  
            
            `
  
            $('#notification-content').append(temp_html)
            $('#notification-content-mobile').append(temp_html)  
          }else{
            let temp_html = `
            <a href="${notification['link']}" class="card-body my-1" style="border-radius:20px; background-color:rgb(248, 252, 255);">
              <small>${times}</small>   
              <p><span><strong>From @${notification['by_user']}:</strong></span> ${notification['message']}</p>
          
            </a>  
            
            `
  
            $('#notification-content').append(temp_html)
            $('#notification-content-mobile').append(temp_html)
  
          }
         
          }}
        else{
          let temp_html = `
          <a class="card-body">
                
            <p>There's nothing here</p>
        
          </a>  
          
          `
          $('#notification-content').empty();
          $('#notification-content-mobile').empty();
          $('#notification-content').append(temp_html)
          $('#notification-content-mobile').append(temp_html)
        }
        
      }
    }

  })  
}
