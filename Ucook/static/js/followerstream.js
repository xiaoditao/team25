// Sends a new request to update the to-do list

function getList() {

    var time = new Date();
    console.log(time.toISOString());
    var list = get_time();
    var isotime;
    if(list.length == 0){
        isotime = "1992-01-01T22:12:11.092834";
    }else{
        isotime = list[0];
    }

    console.log("isotime:"+isotime);
    $.ajax({
        url: "/socialnetwork/refresh-follower?last_refresh="+isotime,
        dataType : "json",
        success: updateList
    });


}

function get_time(){
    var all_time = $("input[id*=last_time]");
    console.log(all_time);

    var list = new Array();
    for(i = 0;i<all_time.length;i++){
        var temp = all_time[i].value;
        list.push(temp);
    }
    list.sort(function(a, b){
		return a < b ? 1 : -1;
	});
    return list;
}

function get_html_comments(){
    var all_posts = $("span[id*=comment_text_]");
    // console.log(all_posts);

    var list = new Array();
    for(i = 0;i<all_posts.length;i++){
        var temp = all_posts[i].id.replace("id_comment_text_","");

        // console.log(temp);
        list.push(temp);
    }
    list.sort(function(a, b){
		return a < b ? 1 : -1;
	});
    return list[0];
}




function updateList(responseText){
    console.log(responseText);


    var posts = responseText.posts;
    var comments = responseText.comments;
        console.log("posts:"+comments[0]);


    var html_comments_num = parseInt(get_html_comments());
    if(isNaN(html_comments_num)){
        html_comments_num = 0;
        console.log("html_comments"+html_comments_num);
    }

    var html_post= document.getElementsByClassName("post_content_text")[0];
    var html_posts_num;
    if(isNaN(html_post)){
        html_posts_num = 0;
        console.log("true");
    }else{
         html_posts_num = parseInt(html_post.id.replace("id_post_text_",""));
    }
        // id.replace("id_post_text_","");

    // console.log(html_posts_num);
    // console.log("comments_num:" +html_comments_num);
    // console.log("posts_num:" +html_posts_num);

    //update posts first:
    $(posts).each(function() {
    // console.log(this);
    // id = this.pk;
    // // postid  = this.fields.post;
    // // username = this.fields.username;
    // text = this.text;
    // console.log(this.user_id);
    // time = this.time;
    var time_format=transfer_time(this.time);
    var id = parseInt(this.id);
    if(id>html_posts_num){

        $(".post_content").prepend(
        " <em>Post by</em>"+
        "<a href='/socialnetwork/profile/"+ this.user_id+"' id='id_comment_profile_"+this.id+"' class='profile_link'>"+this.username+" -</a>"+
        "<span class='post_content_text' id='id_post_text_"+this.id+"'>"+this.text +" -</span> "+
        "<span class='post_time' id='id_post_date_time_'"+this.id+"'>"+time_format+"</span><br>"+
        "<input type ='hidden' id ='last_time' value ='"+this.time+"'>"+
        "<div class = 'comment_content' id = 'comment_content_"+this.id+"'> </div>"+

        "<div><label>Comment by:</label>"+
        "<input id='id_comment_text_"+this.id+"' type='text' name='comment'>"+
        "<button onclick='addcomment("+this.id+"')>submit</button><br><br>"+
        "<span id='error' class='error'></span></div>"

        );
    }


    // console.log("done");
    });





    // var all_text = $("span[id*=text_]");
    // console.log(all_text);
    //
    // var list = new Array();
    // for(i = 0;i<all_time.length;i++){
    //     var temp = all_time[i].value;
    //     list.push(temp);
    // }
    // list.sort(function(a, b){
	// 	return a < b ? 1 : -1;
	// });
    // var isotime = list[1];



    // console.log(posts);
    // console.log(comments[0].post_id);
    // var response = JSON.parse(posts);


     $(comments).each(function() {

       var time_format=transfer_time(this.time);
        var id = parseInt(this.id);
        console.log(id);
        // console.log(this);
        // id = this.pk;
        // postid  = this.fields.post;
        // username = this.fields.username;
        // text = this.fields.text;
        // user = this.fields.user;
        // time = this.fields.time;
        var list =$("#comment_content_"+this.post_id);

        if(id > html_comments_num){
            list.prepend(
                " <em>Comment by</em>"+
                "<a href='/socialnetwork/profile/"+ this.user_id+"' id='id_comment_profile_"+this.user_id+"' class='profile_link'>"+this.username+" -</a>"+
                "<span class='comment_content_text' id='id_comment_text_"+this.id+"'>"+this.text +" -</span> "+
                "<span class='comment_time' id='id_comment_date_time_'"+this.id+"'>"+time_format+"</span><br>"+
                "<input type ='hidden' id ='last_time' value ='"+this.time+"'>"

            );
        }

        console.log("done");
        });

}


function addcomment(post_id) {


    var commentElement = $("input#id_comment_text_"+post_id);

    var commentValue   = commentElement.val();
    var comment_text = encodeURIComponent(commentValue);
    console.log(commentValue);
    // console.log(commentValue);

    // Clear input box and old error message (if any)
    commentElement.val('');
    displayError('');

    $.ajax({
        url: "/socialnetwork/add-comment/"+post_id,
        type: "POST",
        data: "comment="+comment_text+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updateCommentList(response);
            } else {
                displayError(response.error);
            }
        }
    });

}


function updateCommentList(comments){

    $(comments).each(function() {
        console.log(this);
        id = this.pk;

        postid  = this.fields.post;
        username = this.fields.username;
        text = this.fields.text;
        user = this.fields.user;
        time = this.fields.time;
        var list =$("#comment_content_"+postid);
        var timeformat= new Date(time);
        timeformat = timeformat.toLocaleString();
        var newtime = timeformat.substring(0,9)+" "+timeformat.substring(10,14)+" "+timeformat.substring(18,19).toLowerCase()+".m.";
        console.log(newtime);
        console.log(timeformat);

        list.prepend(
            " <em>Comment by</em>"+
            "<a href='/socialnetwork/profile/"+ user+"' id='id_comment_profile_"+user+"'class='profile_link'>"+username+" -</a>"+
            "<span class='comment_content_text' id='id_comment_text_"+id+"'> "+text +" --</span> "+
            "<span class='comment_time' id='id_comment_date_time_"+id+"'>"+newtime+"</span><br>"+
            "<input type ='hidden' id ='last_time' value ='"+time+"'>"
        );
        console.log("done");
        });
}

function transfer_time(time){

    var timeformat= new Date(time);
    timeformat = timeformat.toLocaleString();
    var newtime = timeformat.substring(0,9)+" "+timeformat.substring(10,14)+" "+timeformat.substring(18,19).toLowerCase()+".m.";
    return newtime;
}





function displayError(message) {
    var errorElement = document.getElementById("error");
    errorElement.innerHTML = message;
}



function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        c = cookies[i].trim();
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}






// The index.html does not load the list, so we call getList()
// as soon as page is finished loading
window.onload = getList;

// causes list to be re-fetched every 5 seconds
window.setInterval(getList, 5000);