odoo.define('odoo_ask.ask_create_dialog', function(require) {
    "use strict";
    var ListController = require('web.ListController');
    var viewRegistry = require('web.view_registry');
    var ListView = require('web.ListView');

    var AskListController = ListController.extend({
        _onCreate: function() {
            this.do_action('odoo_ask.action_ask_wizard');
        }
    });

    var AskListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: AskListController,
        }),
    });

    viewRegistry.add('ask_list_override', AskListView);
});
