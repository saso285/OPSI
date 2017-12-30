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

    function ajaxPostHttpRequest(url, data) {
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
                'text': elem,
                'state':
                {
                    'opened': false,
                },
                'children': [],
                "data":
                {
                    'field': elem
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
        modalTitle.empty();
        modalTitle.text(data.node.text);
        modalTag.empty();
        modalTag.text(data.node.data.format);
        modalTimestamp.empty();
        modalTimestamp.text(data.node.data.revision_id);
        modalBody.empty();
        modalBody.append('<p id="modal-description"></p>');
        $('#modal-description').text(data.node.data.notes);
        if (data.node.data.name != undefined) {
            modalBody.append('<a href="/file/' + data.node.data.name + '">' + data.node.data.name + '</a><br>');
        }
        modal.modal('show');
    }

    function buildSubtree() {
        tree.on("select_node.jstree", function(e, data) {
            if (!data.node.state.opened) {
                if (data.node.parent === '#' && data.node.children.length == 0) {
                    ajaxPostHttpRequest('/fields', {'field': data.node.data.field}).result.forEach(function(elem) {
                        tree.jstree("create_node", '#' + data.node.id, {'text': elem, 'data': {'label': elem, 'type': 'folder'}});
                    });
                } else if (data.node.data.type === 'folder' && data.node.children.length === 0) {
                    var resp = ajaxPostHttpRequest('/files', data.node.data).result;
                    var json;
                    resp.forEach(function(item) {
                        var subJson;
                        subJson = {'type': 'file', 'url': item.url, 'name': item.name, 'format': item.type, 'revision_id': item.revision_id}
                        json = {'text': item.name, 'icon': 'jstree-file', 'data': subJson};
                        tree.jstree("create_node", '#' + data.node.id, json);
                    });
                    if (resp.length === 0) {
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