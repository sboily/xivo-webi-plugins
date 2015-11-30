var ws = new SockJS(bus_host);

ws.onmessage = function(m) {
    raw = $.parseJSON(m.data)
    on_status_change(raw.data);
    ack = {
        'ack': true
    }
    ws.send(JSON.stringify(ack));
}

ws.onopen = function() {
    token = {
        'token': token
    }
    ws.send(JSON.stringify(token));
};

ws.onclose = function() {
     console.log('Connection close');
     ws.close();
};

var on_status_change = function(s) {
    update_color_box(s.endpoint_id, parseInt(s.status, 10));
}

var find_box = function(endpoint_id) {
    box = $('.box[data-line="' + endpoint_id +'"]')
    return box;
}

var update_color_box = function(endpoint_id, endpoint_status) {
    color = set_color_on_status(endpoint_status);
    box = find_box(endpoint_id);
    clean_color_box(box);
    box.addClass(color);
}

var clean_color_box = function(box) {
    box.removeClass(function (index, css) {
        return (css.match (/(^|\s)box-\S+/g) || []).join(' ');
    });
}

var set_color_on_status = function(endpoint_status) {
    if (endpoint_status == 1)
        color = "box-danger";
    else if (endpoint_status == 0)
        color = "box-success";
    else if (endpoint_status == 4)
        color = "box-danger";
    else {
        color = "box-warning";
    }

    return color
}
