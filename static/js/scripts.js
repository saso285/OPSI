$(document).ready(function() {

    var tree = $('#tree');
    var modal = $('#modal');
    var modalTitle = $('.modal-title');
    var modalTimestamp = $('#modal-timestamp');
    var modalTag = $('#modal-tag');
    var modalBody = $('.modal-body');
    var node = $('.jstree-clicked');

    function ajaxGetHttpRequest(url) {
        var response;
        $.ajax({
            type: 'GET',
            url: url,
            contentType: 'application/json',
            dataType: 'json',
            async: false,
            success:function(res){
                response = res;
            },
            error:function(res){
                console.log(res);
            }
        });
        return response;
    }

    function ajaxGetPostRequest(url, data) {
        var response;
        $.ajax({
            type: 'POST',
            url: url,
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(data),
            async: false,
            success:function(res){
                response = res;
            },
            error:function(res){
                console.log(res);
            }
        });
        return response;
    }

    function buildTree() {
        var ex = {};
        ex.core = {'check_callback': true};
        ex.core.data = [];
        ajaxGetHttpRequest('/fields').result.forEach(function(elem) {
            ex.core.data.push(
            {
                'text': elem[0],
                'state':
                {
                    'opened': false,
                },
                'children': [],
                "data":
                {
                    'url': elem[1]
                }
            }); 
        });
        tree.jstree(ex);
    }

    function open_node(id) {
        setTimeout(function(){
            tree.jstree("open_node", $("#" + id));
        }, 100);
    }

    function close_node(id) {
        setTimeout(function(){
            tree.jstree("close_node", $("#" + id));
        }, 100);
    }

    function create_modal(data) {
        console.log(data.node.data)
        modalTitle.empty();
        modalTitle.text(data.node.text);
        modalTag.empty();
        modalTag.text(data.node.data.format);
        modalTimestamp.empty();
        modalTimestamp.text(data.node.data.timestamp);
        modalBody.empty();
        modalBody.append('<p id="modal-description"></p>');
        $('#modal-description').text(data.node.data.notes);
        if (data.node.data.name != undefined) {
            modalBody.append('<a href="' + data.node.data.url + '">' + data.node.data.name + '</a><br>');
        }
        modal.modal('show');
    }

    function buildSubtree() {
        tree.on("select_node.jstree", function(e, data) {
            if (!data.node.state.opened) {
                if (data.node.parent === '#' && data.node.children.length == 0) {
                    ajaxGetPostRequest('/fields', {'url': data.node.data.url}).result.forEach(function(elem) {
                        tree.jstree("create_node", '#' + data.node.id, {'text': elem[0], 'data': {'label': elem[1], 'type': 'folder'}});
                    });
                } else if (data.node.data.type === 'folder' && data.node.children.length === 0) {
                    var resp = ajaxGetPostRequest('/field', data.node.data).result;
                    var json;
                    resp.resources.forEach(function(item) {
                        var subJson;
                        var name = item.name || item.description;
                        var timestamp = "";
                        if (resp.revision_timestamp != undefined) {
                            timestamp = resp.revision_timestamp.split("T")[0].split("-");
                            timestamp = "Last revision: " + timestamp[2] + "." + timestamp[1] + "." + timestamp[0];
                        }
                        subJson = {'type': 'file', 'notes': resp.notes, 'url': item.url, 'name': name, 'format': item.format, 'timestamp': timestamp}
                        json = {'text': name, 'icon': 'jstree-file', 'data': subJson};
                        tree.jstree("create_node", '#' + data.node.id, json);
                    });
                    if (resp.resources.length === 0) {
                        data.node.data.notes = resp.notes;
                        create_modal(data);
                    }
                } else if (data.node.data.type === 'file') {
                    create_modal(data)
                }
                open_node(data.node.id);
            } else {
                close_node(data.node.id);
            }
        });
    }

    buildTree();
    buildSubtree();
});