/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/people',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(id, fname, lname, email) {
            let ajax_options = {
                type: 'POST',
                url: 'api/people',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'id': id,
                    'fname': fname,
                    'lname': lname,
                    'email': email
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(id, fname, lname, email) {
            let ajax_options = {
                type: 'PUT',
                url: 'api/people/' + id,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'id': id,
                    'fname': fname,
                    'lname': lname,
                    'email': email
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(id) {
            let ajax_options = {
                type: 'DELETE',
                url: 'api/people/' + id,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $id = $('#id'),
        $fname = $('#fname'),
        $lname = $('#lname'),
        $email = $('#email')
	;

    // return the API
    return {
        reset: function() {
            $id.val('').focus();
            $fname.val('');
            $lname.val('');
            $email.val('');
        },
        update_editor: function(id, fname, lname, email) {
            $id.val(id).focus();
            $fname.val(fname);
            $lname.val(lname);
            $email.val(email);
        },
        build_table: function(people) {
            let rows = ''

            // clear the table
            $('.people table > tbody').empty();

            // did we get a people array?
            if (people) {
                for (let i=0, l=people.length; i < l; i++) {
                    rows += `<tr><td class="id">${people[i].id}</td><td class="fname">${people[i].fname}</td><td class="lname">${people[i].lname}</td><td class="email">${people[i].email}</td><td>${people[i].timestamp}</td></tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $id = $('#id'),
        $fname = $('#fname'),
        $lname = $('#lname'),
        $email = $('#email');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(id, fname, lname, email) {
        return id !== "" && fname !== "" && lname !== "" && email !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let id = $id.val(),
            fname = $fname.val(),
            lname = $lname.val(),
            email = $email.val();

        e.preventDefault();

        if (validate(id, fname, lname, email)) {
            model.create(id, fname, lname, email)
        } else {
            alert('Problem with first or ID input');
        }
    });

    $('#update').click(function(e) {
        let id = $id.val(),
            fname = $fname.val(),
            lname = $lname.val(),
            email = $email.val();

        e.preventDefault();

        if (validate(id, fname, lname, email)) {
            model.update(id, fname, lname, email)
        } else {
            alert('Problem with first or ID input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let id = $id.val();

        e.preventDefault();

        if (validate('placeholder', id)) {
            model.delete(id)
        } else {
            alert('Problem with first or ID input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            id,
            fname,
            lname,
            email;

        id = $target
            .parent()
            .find('td.id')
            .text();

        fname = $target
            .parent()
            .find('td.fname')
            .text();

        lname = $target
            .parent()
            .find('td.lname')
            .text();

        email = $target
            .parent()
            .find('td.email')
            .text();

        view.update_editor(id, fname, lname, email);
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));


