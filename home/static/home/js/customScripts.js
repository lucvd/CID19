$(document).ready(function () {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');


    function clickedFilter(button) {
        var tagTitle = button.attr("data-btn-tag-title");
        var active = button.hasClass("filter-on"); // Inverted because the active part is added after the clicked function runs

        $(".homepage-card-container").each(function () {
            var container = $(this);

            container.find(".homepage-card-tag").each(function () {
                var tagspan = $(this);
                var filterCounter = tagspan.closest(".homepage-card-container").find(".homepage-card-tag-filter-counter");
                var currentCount = +filterCounter.text();
                var plusOne = currentCount + 1;
                var minusOne = currentCount - 1;

                if (active) {
                    if (tagspan.html() === tagTitle) {
                        filterCounter.text(plusOne);
                    }
                } else {
                    if (tagspan.html() === tagTitle) {
                        filterCounter.text(minusOne);
                    }
                }
            });


            if (container.find(".homepage-card-tag-filter-counter").html() === "0") {
                container.hide();
            } else {
                container.show();
            }


        });

        runFilterCount()
    }

    function runFilterCount(){
        // reset filters if everything
        var active_filter_count = 0;
        $(".tag-filter-button").each(function () {
            if ($(this).hasClass("filter-on"))
                active_filter_count++;
        });
        if (active_filter_count === 0) {
            $(".homepage-card-container").show();
        }

        //manage favorites
        var showfavorites = $('#favorite-button').hasClass("btn-primary");

        $(".homepage-card-container").each(function () {
            var container = $(this);

            var isfavorite = container.find(".home-favorite-button").hasClass("isfavorite");

            // hide if showFavorites is true and it is not a favorite
            if (showfavorites && !isfavorite) {
                container.hide();
            }

            if (!showfavorites && active_filter_count !== 0) {
                if (container.find(".homepage-card-tag-filter-counter").html() !== "0") {
                    container.show();
                }
            }
        });
    }


    $(".tag-filter-category").click(function() {
        var categoryButton = $(this);
        var deactivate = categoryButton.hasClass("active");


        // make every button active and apply the filter for every button
        categoryButton.parent().find(".tag-filter-button").each(function(){
            var button = $(this);
            if (deactivate) {
                button.removeClass("active");
                button.removeClass("filter-on");
            } else {
                button.addClass("active");
                button.addClass("filter-on");
            }
            clickedFilter(button);
        })

    });


    $(".tag-filter-button").click(function () {
        var button = $(this);
        if (button.hasClass("filter-on")) {
            button.removeClass("filter-on");
        } else {
            button.addClass("filter-on");
        }

        clickedFilter(button);
    });

    $("#reset-filters").click(function () {
        $(".tag-filter-button").removeClass("active");
        $(".tag-filter-button").removeClass("filter-on");
        $(".homepage-card-container").show();
        $(".homepage-card-tag-filter-counter").each(function () {
            $(this).html(0);
        });
        $(".tag-filter-category").removeClass("active");
        $(".tag-filter-category").removeClass("filter-on");

        var  favbtn = $("#favorite-button");
        favbtn.removeClass("btn-primary");
        favbtn.addClass("btn-outline-primary");
    });

    $("#favorite-button").click(function () {
        var favbtn = $(this);
        var showfavorites = favbtn.hasClass("btn-outline-primary");

        if (showfavorites){
            favbtn.removeClass("btn-outline-primary");
            favbtn.addClass("btn-primary")
        } else {
            favbtn.removeClass("btn-primary");
            favbtn.addClass("btn-outline-primary");
        }

        runFilterCount();

    });


    $(".home-favorite-button").click(function () {

        var projectID = $(this).attr('id');

        $.ajax({
            type: 'POST',
            url: '/ajax/togglefavorite/',
            contentType: 'application/json',
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            data: JSON.stringify({
                'projectID': projectID
            }),
            success: favorite_button_clicked_success,
            error: function (result) {
                alert("Error marking favorite, check internet connectivity!");
            }
        });
    });

    function favorite_button_clicked_success(result) {
        var projectID = result["projectID"];
        var favoritebutton = $("#" + projectID);

        favoritebutton.toggleClass("btn-primary btn-secondary");

        if (favoritebutton.hasClass("btn-primary")) {
            favoritebutton.text("Remove as favorite");
            favoritebutton.addClass("isfavorite");
        } else {
            favoritebutton.text("Mark as favorite");
            favoritebutton.removeClass("isfavorite");
        }
    }

    $("#remove-project-button").click(function () {
        var projectNameGuess = $("#probablyProjectName").val();
        var feedback = $("#feedback-remove-project").val();
        var projectID = $(".home-favorite-button").attr("id");
        $.ajax({
            type: 'POST',
            url: '/ajax/deleteproject/' + projectID + '/',
            contentType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            data: JSON.stringify({
                'projectNameGuess': projectNameGuess,
                'feedback': feedback
            }),
            success: remove_project_success,
            error: function (result) {
                alert("Error removing project, check internet connectivity!");
            }
        });
    });

    $("#probablyProjectName").on("change keyup paste", function(){
        var projectNameGuess = $(this).val();
        var removeButton = document.getElementById("remove-project-button");
        var projectTitle = $("#project-title").val();
        if(projectNameGuess === projectTitle)
        {
            removeButton.style.background="#dc3545";
            removeButton.disabled = false;
        }
        else
        {
            removeButton.style.background="darkgray";
            removeButton.disabled = true;
        }

    });

    function remove_project_success(result) {
        var removed = result['removed'];
        window.location.href="/projects";
    }

    $("#id_generalProjectType").on("change", function(){
       let generalSelected = $(this).val();
       let projectType = $("#id_projectType");

       if(generalSelected === '')
       {
           $("#id_projectType > option").each(function(){
                if(this.value !== "")
                {
                    $(this).hide();
                }
            });
            projectType.val(0);
       }
       else
       {
            $("#id_projectType > option").each(function(){
                if(this.value !== "")
                {
                    if(this.value.includes(generalSelected))
                    {
                        $(this).show();
                    }
                    else {
                        $(this).hide();
                    }
                }
            });
            projectType.val(0);
       }
    }).change();

    $("#add-keyword").click(function(){
        let new_keyword = $("#id_keywords").val();
        for(let i=1; i<6; i++)
        {
            let btn = $("#keyword-button-" + i);
            if(btn.text() === "")
            {
                btn.text(new_keyword);
                btn.show();
                break;
            }
        }
    });

    $("#keyword-button-1").click(function(){
        $(this).text("");
        $(this).hide();
    });

    $("#keyword-button-2").click(function(){
        $(this).text("");
        $(this).hide();
    });

    $("#keyword-button-3").click(function(){
        $(this).text("");
        $(this).hide();
    });

    $("#keyword-button-4").click(function(){
        $(this).text("");
        $(this).hide();
    });

    $("#keyword-button-5").click(function(){
        $(this).text("");
        $(this).hide();
    });

});
