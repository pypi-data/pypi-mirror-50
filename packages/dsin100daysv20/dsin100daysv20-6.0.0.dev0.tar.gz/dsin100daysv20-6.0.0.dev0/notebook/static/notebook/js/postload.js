// Adds a button to hide the input part of the currently selected cells

define([
    'jquery',
    'base/js/namespace',
    'base/js/events',
    'base/js/utils',
], function(
    $,
    Jupyter,
    events,
    utils
) {
    "use strict";
    // NOTE: all the functions should be idempotent, i.e on multiple load of same
    // function should have same behaviour
    
    var load = true;
    var initialized_logout = false;

    function hide_download_options() {
        $('#download_menu > li:not(:last-child)').hide();
        $('#download_ipynb').show();
    }

    function get_git_pull_url() {
        var hub_user_url = '/hub/user-redirect';
        var repo_url = 'https://github.com/colaberry/dsin100days';
        var branch = 'master';
        var subpath = Jupyter.notebook.notebook_path.replace('dsin100days/', '');
        subpath = encodeURIComponent(subpath);
        var url = hub_user_url + '/git-pull?repo=' + repo_url + '&branch=' + branch + '&subPath=' + subpath;
        return url;
    }

    function add_update_link() {
        if($("#update_files").length == 0) {
            var url = get_git_pull_url();
            var html = '<li class="dropdown" id="update_files"><a href="#"class="dropdown-toggle" data-toggle="dropdown">Update</a>';
            // update_files link doesn't exist, so append it.
            $('.navbar-nav').append(html);
            $('#update_files').on('click', function(e) {
                window.location.href = url;
            });
        }
    }

    function nbbkp() {
        var data = Jupyter.notebook.toJSON();
        for (var i=0; i<data.cells.length; i++) {
            if (data['cells'][i].outputs !== undefined) {
                data['cells'][i].outputs = [];
            }
        }
        var username = /user\/([^/]+)\//.exec(Jupyter.notebook.base_url)[1];
        var arr = {'username': username, 'path': Jupyter.notebook.notebook_path, 'data': data};
        $.ajax({
            url: 'http://db.colaberry.cloud:8000/save',
            type: 'POST',
            data: JSON.stringify(arr),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
        });
    }

    function add_uuids_for_cells() {
        var cells = Jupyter.notebook.get_cells();
        for(var i=0; i<cells.length; i++) {
            if(!cells[i].metadata['cell_id']) {
                cells[i].metadata['cell_id'] = utils.uuid();
            }
        }
    }

    function stackdriver_log_cell_output() {
        events.on('output_added.OutputArea', function (e, d) {
            if (d.output_area['outputs'][0]['output_type'] == 'error') {
                var output = d.output;
                var i = d.output_area.element.closest('.cell').index();
                var cell_id = Jupyter.notebook.get_cell(i).metadata.cell_id;
                var data = {'cell_output': output, 'cell_id': cell_id};
                $.ajax({
                    url: 'http://mw.colaberry.cloud/stackdriver/write/entries',
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    error: function(resp) {
                        console.log('stackdriver log error', resp);
                    }
                });
            }
        });
    }

    function change_logo() {
      $('#ipython_notebook a img').attr('src', 'https://s3.amazonaws.com/refactored/images/refactored_logo.svg');
    }

    function injectScript(src) {
      return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.async = true;
        script.src = src;
        script.addEventListener('load', resolve);
        script.addEventListener('error', () => reject('Error loading script.'));
        script.addEventListener('abort', () => reject('Script loading aborted.'));
        document.head.appendChild(script);
      });
    }

    function logout() {
      injectScript('https://cdn.auth0.com/js/auth0/9.10/auth0.min.js')
        .then(() => {
          if (window.location.origin === "http://dsin100days.colaberry.cloud") {
            var domain = 'refactored-ai.auth0.com';
            var client_id = 'r6kyUXHfPo7uQYm5PuM9BUo40eDKhbjW';
            var redirect_uri = 'http://dsin100days.colaberry.cloud/hub/oauth_callback';
          } else if (window.location.origin === "http://stage.dsin100days.colaberry.cloud") {
            var domain = 'rfmagiclink.auth0.com';
            var client_id = 'adLF2VIdkq1RclhcKi44B3HRWyQojKFX';
            var redirect_uri = 'http://stage.dsin100days.colaberry.cloud/hub/oauth_callback';
          }
          function logoutinterval() {
            var webAuth = new auth0.WebAuth({
              domain: domain,
              clientID: client_id,
              redirectUri: redirect_uri,
              responseType: 'token'
            });
            webAuth.checkSession({}, function (err, res) {
              console.log(err, res);
              if (err.code == 'login_required') {
                window.location.href = '/user/'+/user\/([^/]+)/.exec(Jupyter.notebook.base_url)[1]+'/logout';
              }
              console.log(err, res);
            });
          }
          setInterval(logoutinterval, 10000);
        }).catch(error => {
          console.log(error);
        });
    }

    function load_functions() {
        if (load) {
            add_uuids_for_cells();
            change_logo();
            hide_download_options();
            add_update_link();
            stackdriver_log_cell_output();
            if (initialized_logout === false) {
              logout();
              initialized_logout = true;
            }
            events.on('notebook_saved.Notebook', nbbkp);
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
