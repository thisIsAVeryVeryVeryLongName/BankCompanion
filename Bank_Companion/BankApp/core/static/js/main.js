var callAJAX = true;

// AJAX PREPARE FUNCTIONS
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Prepares AJAX header for Django
function prepareAjax() {
    // Get CSRF Token
    var csrftoken = $("#csrf-form input[name=csrfmiddlewaretoken]").val();
    // Prepare POST header
    $(document).ajaxSend(function(event, xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !settings.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
}

// On submit, this function catches the submet event of forms with class 'catched' and sends instead a ajax request
function catchForms() {
    $('form.catched').on('submit', function(e) {
        e.preventDefault();
        $('#pagination-loading-spinner').show();
        prepareAjax();
        var ajaxUrl = $(this).attr('action');
        if (typeof ajaxUrl == 'undefined' || ajaxUrl == '') { ajaxUrl = window.location.pathname; }
        $(this).ajaxSubmit({  //previous: $(this).appendTo("body")ajaxSubmit({  ;but removed because it puts a form at the end of the body-tag
            url: ajaxUrl,
            success: function(data, textStatus, xhr) {
                $(this).detach();
                response_url=xhr.getResponseHeader('X-URL')
                console.log('success '+xhr.status+' url '+response_url);
                if(xhr.status == 204)//check if answer is empty
                {
                    console.log('catchForm reload '+window.location.href);
                    load_page(window.location.href);
                }
                else if (response_url!=ajaxUrl) { //check if redirected
                    // data.redirect contains the string URL to redirect to
                    // window.location.href = data.redirect;
                    console.log('catchForm redirect to '+response_url);
                    console.log('data: '+data);
                    load_page(response_url);
                }
                else {
                    GO_TO_TOP = false;
                    console.log('catchForm load content '+ajaxUrl);
                    console.log('data.redirect: '+response_url);
                    update_content(data,ajaxUrl);
                }
                snackBar('Saved successfully!');
            }
        });
    });
}

// If the URL was called via browsers back/forward button, it will get set true to prevent history override in the load_page() function
var popstate = false;

// If the content should scroll to top after load_page
var GO_TO_TOP = true;

// Main page load ajax function
function load_page(page_url) {
    
    cur_url = page_url;
    console.log('load_page url '+page_url);
    
    prepareAjax();

    $.ajax({
        async: true,
        type: "POST",
        url: page_url,
        xhrFields: { withCredentials: true },
        dataType: 'html',
        error: function(data){
            $('#content').html('<h3>Something went wrong :(</h3><br /><br />Response ');
            var txt = "<table>"
            for (x in data) {
                txt += "<tr><td>" + data[x] + "</td></tr>";
            }
            console.log(data);
            txt += "</table>" 
            document.getElementById("content").innerHTML += txt;
            $('body').toggleClass('show-nav');
            window.history.pushState(null, null, page_url);
            GO_TO_TOP = true;
        },
        success: function(data, textStatus, xhr){
            response_url=xhr.getResponseHeader('X-URL')
            console.log('success '+xhr.status+' url '+response_url);
            if (response_url!=page_url) { //check if redirected
                console.log('load_page redirect to '+response_url);
                load_page(response_url);
                GO_TO_TOP = true;
            }
            else {
                console.log('load_page load content '+page_url);
                update_content(data,page_url);
            }
            if ($('body').hasClass('show-nav')) {
                $('#top-nav-container').fadeIn(150);
            } else {
                $('#top-nav-container').fadeOut(150);
            }
        }
    });
}



// Updates the content
function update_content(response,page_url){
    old_dest=window.location.href
    $('#content').html(response);
    if ($('body').hasClass('show-nav')) {
        $('body').toggleClass('show-nav');
    }
    if (!popstate) { window.history.pushState(null, null, page_url);popstate = false }
    GO_TO_TOP = (window.location.href!=old_dest);//only go to top when url changes
    rerunJS();
    catchForms();
    $('#main-nav').find('button').removeClass('active');
    if (cur_url.localeCompare('/outgoing-transaction-list/')==0) {
        $('#outgoing button').addClass('active');
    } else if (cur_url.localeCompare('/incoming-transaction-list/')==0) {
        $('#incoming button').addClass('active');
    } else if (cur_url.localeCompare('/account-list/')==0) {
        $('#transactions button').addClass('active');
    }
}

// Rerun on every page load
function rerunJS() {
    // Checks for new transactions
    prepareAjax();
    GO_TO_TOP = false;
    // Send POST request
    $.ajax({
        async: true,
        type: "POST",
        url: "/unasigned-transaction/",
        traditional: true,
        success: function(response) {
            if (!(response == 'none')) {
                $('#main-overlay').fadeIn();
                $('#main-overlay').html(response);
            }
        },
        error: function(data) {console.log(data)}
    });
}

// Hides the Overlay
function hideOverlay() {
    $('#main-overlay').fadeOut();
    setTimeout(function() {$('#main-overlay').html(''), 200});
}

// On first load, trigger the load_page() function
if (callAJAX) {
    load_page(window.location.pathname);
}

// Onpopstate event, called when browsers back/forward button was pushed
window.onpopstate = function(event) {
    popstate = true;
    load_page(window.location.pathname);
}
