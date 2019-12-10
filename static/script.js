"use strict";

function update_ratings(){
    $.ajax({
        url: "/get_ratings",
        method:"GET",
        success: function(data) {
            if (data != "False"){
                var vals = JSON.parse(data);
                console.log(vals);
                $("#table tbody > tr").remove();
                for (var key in vals){
                    $('#table tbody').append('<tr><td>' + key + '</td><td>' + 
                        vals[key][1] + '</td><td>' + vals[key][2] + 
                        '</td><td>' + vals[key][0] + '</td></tr>');
                }
            } 
        }
    });
    
}

function login(username) {
    $("#login").toggle();
    $("#main").toggle();
    $("#username_main").val(username);
    update_ratings();

}

$( document ).ready(function(event){
    $("#form_login").submit( function(event){
        event.preventDefault();
        var signup_val = 0;
        if ($('#signup').is(":checked")){
            signup_val = 1;
        };
        console.log(signup_val)
        $.ajax({
            url: "/login",
            data: {
                username: $("#username").val(),
                password: $("#password").val(),
                signup: signup_val
            },
            method:"get",
            success: function(data) {
                if (data != "False"){
                    login($("#username").val());
                } else {
                    window.alert("Incorrect username or password, please try again.")
                }
            }
          });
    });

    $("#form_user").submit( function(event){
        event.preventDefault();
        var name = $("#username_main").val()
        $.ajax({
            url: "/update_details",
            data: {
                username: $("#username_main").val()
            },
            method:"post",
            success: function(data) {
                if (data != "False"){   
                    $("#username_main").val(name);
                }
            }
          });
    });

    $("#form_rating").submit( function(event){
        event.preventDefault();
        console.log($("#bookid").val());
        console.log($("#rating").val());
        $.ajax({
            url: "/make_rating",
            data: {
                bookid: $("#bookid").val(),
                rating: $("#rating").val()
            },
            method:"post",
            success: function(data) {
                update_ratings();
            }
          });
    });
})