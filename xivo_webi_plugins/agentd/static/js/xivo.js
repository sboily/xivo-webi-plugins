var ws = new SockJS(bus_host);
var client = Stomp.over(ws);

client.heartbeat.incoming = 0;
client.heartbeat.outgoing = 0;


var onmessage = function(m) {
    raw = $.parseJSON(m.body)
    events_agent_status(raw.data);
}

var on_connect = function(x) {
    id = client.subscribe("/exchange/xivo/status.agent", onmessage);
};

var on_error =  function() {
    console.log('error');
};

var append_unlog_action = function() {
    return "<p id='action' class='unlog'><a href='#'>unlog</a></p>";
};

var append_log_action = function() {
    return "<p id='action' class='log'><a href='#'>log</a></p>";
};

var remove_unlog_action = function(e) {
    $("#" + e + " #action").remove();
};

var is_logged = function(e) {
    return(((e) == true || (e) == "logged_in" ? true : false));
};

var events_agent_status = function(e) {
    $("#" + e.agent_id).effect("shake", "slow");
    $("#" + e.agent_id + " #status")
      .text("Logged: " + ((e.status) == "logged_in" ? true : false));

    if (!is_logged(e.status)) {
        remove_unlog_action(e.agent_id);
        $("#" + e.agent_id).append(append_log_action(e.agent_id));
    }
    else {
        remove_unlog_action(e.agent_id);
        $("#" + e.agent_id).append(append_unlog_action(e.agent_id));
    }
};

var unlog = function(id) {
    var client = new $.RestClient("/x/");

    client.add("agentd", { stripTrailingSlash: true });
    client["agentd"].read(id);
};

var log = function(id) {
    var client = new $.RestClient("/x/");

    dialog.dialog("close");
    data = {context: $(context).val() , extension:  $(extension).val() };
    client.add("agentd", { stripTrailingSlash: true });
    client["agentd"].create(id, data);
};

var unpause = function(number) {
    var client = new $.RestClient("/x/");

    client.add("agentd");
    client.agentd.add("unpause");
    client.agentd.unpause.read(id);
};

var pause = function(number) {
    var client = new $.RestClient("/x/");

    client.add("agentd");
    client.agentd.add("agentd");
    client.agentd.pause.create(number);
};
var get_context_extension = function() {
    dialog.dialog("open");
}

client.debug = function(e) {};

$(function() {
    client.connect(bus_username, bus_password, on_connect, on_error, '/');
    $(document).on("click", "a" , function() {
        id = ($(this).parent().parent().attr('id'));
        action = $(this).parent().attr('class');
        if (action == 'log')
            get_context_extension()
        else if (action == 'unlog')
            unlog(id);
    });

    $('.gridly').gridly({
      base: 60,
      gutter: 20,
      columns: 10
    });

    dialog = $("#dialog-form")
               .dialog({ autoOpen: false, 
                         height: 400,
                         width: 450,
                         modal: true,
                         buttons: {
                             "Login agent": function() { log(id); },
                             Cancel: function() { dialog.dialog("close"); }
                         }
                       });

});
