// Adds a button to hide the input part of the currently selected cells

define([
    'jquery',
    'base/js/namespace',
    'base/js/events',
    'notebook/js/auth0',
], function(
    $,
    Jupyter,
    events,
    auth0,
) {
    "use strict";
    // NOTE: all the functions should be idempotent, i.e on multiple load of same
    // function should have same behaviour
    
    var load = true;
    if (window.location.origin === "http://dsin100days.colaberry.cloud") {
      var domain = 'refactored-ai.auth0.com';
      var client_id = 'r6kyUXHfPo7uQYm5PuM9BUo40eDKhbjW';
      var redirect_uri = 'http://dsin100days.colaberry.cloud/hub/oauth_callback';
    } else if (window.location.origin === "http://stage.dsin100days.colaberry.cloud"){
      var domain = 'rfmagiclink.auth0.com';
      var client_id = 'adLF2VIdkq1RclhcKi44B3HRWyQojKFX';
      var redirect_uri = 'http://stage.dsin100days.colaberry.cloud/hub/oauth_callback';
    } else if (window.location.origin === "http://localhost:8888"){
      var domain = 'rfmagiclink.auth0.com';
      var client_id = 'adLF2VIdkq1RclhcKi44B3HRWyQojKFX';
      var redirect_uri = 'http://localhost:8888/hub/oauth_callback';
    }
    var webAuth = new auth0.WebAuth({
      domain: domain,
      clientID: client_id,
      redirectUri: redirect_uri,
      responseType: 'token'
    });

    function logout() {
      webAuth.checkSession({}, function (err, res) {
        console.log(err, res);
        if (err !== null && err.code == 'login_required') {
          window.location.href = '/user/'+/user\/([^/]+)/.exec(Jupyter.notebook.base_url)[1]+'/logout';
        }
      });
    }

    function load_functions() {
        if (load) {
            setInterval(logout, 60000);
            load = false;
        }
    }

    var load_extension = function() {
        if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
            load_functions();
        }
        events.on("notebook_loaded.Notebook", load_functions);
    };

    return {
        load_extension : load_extension
    };
});
