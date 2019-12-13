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

function get_recommendations(){
    $.ajax({
        url: "/get_recoms",
        method:"GET",
        success: function(data) {
            if (data != "False"){
                var vals = JSON.parse(data);
                console.log(vals);
                $("#table2 tbody > tr").remove();
                for (var key in vals){
                    $('#table2 tbody').append('<tr><td>' + key + '</td><td>' + 
                        vals[key][0] + 
                        '</td><td>' + vals[key][1] + '</td></tr>');
                }
            } 
        }
    });
}

function login(username) {
    $("#login").toggle();
    $("#main").toggle();
    $("#nav").toggle();
    $("#username_main").val(username);
    update_ratings();
    get_recommendations();

}

function logout(){
    $.ajax({
        url: "/logout",
        method:"POST",
        success: function(data) {
            if (data != "False"){
                logout_change();
            }
        }
        })
}

function logout_change(){
    $("#login").toggle();
    $("#main").toggle();
    $("#nav").toggle();
}

function toggle_nation(){
    console.log($("#nation").html());
    var nation = $("#nation").html();
    if (nation == "Spanish"){
        update_language(1);
    } else {
        update_language(2);
    }
}

function update_label(value){
    if (value == "False"){
        if ($("#nation").html() == "Spanish"){
            $("#outLabel").html("El libro no fue encontrado.");
        } else {
            
            $("#outLabel").html("The book was not found.");
        };
    } else {
        if ($("#nation").html() == "Spanish"){
            
            $("#outLabel").html("Ese libro tiene ID: " + value);
        } else {
            $("#outLabel").html("That book has ID: " + value);
        };
    }
}

function update_language(val){
    if (val == 1){
        var labels = trans_vals["en"];
        $("#nation").html("English")
    } else { 
        var labels = trans_vals["sp"];
        $("#nation").html("Spanish")
    }

    $("#signin-text").html(labels[0]);
    $("#signup").html(labels[1]);
    $("#signin-button").html(labels[2]);
    $("#button-logout").html(labels[3]);
    $("#username-label").html(labels[4]);
    $("#username-details").html(labels[5]);
    $("#rating-label").html(labels[6]);
    $("#remove-tag").html(labels[7]);
    $("#confirm-button").html(labels[8]);
    $("#label-addbook").html(labels[9]);
    $("#confirm-button2").html(labels[10]);
    $("#label-main").html(labels[11]);
    $("#tag-book").html(labels[12]);
    $("#tag-name").html(labels[13]);
    $("#tag-genre").html(labels[14]);
    $("#label-recom").html(labels[15]);
    $("#tag-book2").html(labels[16]);
    $("#tag-name2").html(labels[17]);
    $("#tag-genre2").html(labels[18]);
    $("#name").attr("placeholder", labels[19]);
    $("#genre").attr("placeholder", labels[20]);
    $("#bookid").attr("placeholder", labels[21]);
    $("#username").attr("placeholder", labels[22]);
    $("#password").attr("placeholder", labels[23]);
    $("#tag-rating").html(labels[24]);
    $("#label-searchbook").html(labels[25])
    $("#searchname").attr("placeholder", labels[26])
    $("#search-button").html(labels[27])
}



$( document ).ready(function(event){
    $("#button").click( function() {
        logout();
    });
    $("#nation").click( function() {
        toggle_nation();
    });
    $("#button-logout").click( function() {
        $.ajax({
            url: "/login",
            method:"post",
            success: function(data){
                location.reload()
            }
        });
    });

    $("#form_login").submit( function(event){
        event.preventDefault();
        var signup_val = 0;
        if ($('#signup').is(":checked")){
            signup_val = 1;
        };
        console.log(signup_val);
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

    $("#form-search").submit( function(event){
        event.preventDefault();
        $.ajax({
            url: "/search_books",
            data: {
                bookname: $("#searchname").val()
            },
            method:"get",
            success: function(data) {
                update_label(data);
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

    $("#form_book").submit( function(event){
        event.preventDefault();
        console.log($("#name").val());
        console.log($("#genre").val());
        $.ajax({
            url: "/add_book",
            data: {
                bookname: $("#name").val(),
                genre: $("#genre").val()
            },
            method:"post",
            success: function(data) {
                window.alert("Book has been added. ID:"+data)
            }
          });
    });
    toggle_nation();
})