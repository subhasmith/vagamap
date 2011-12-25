/**
 * Plugin designed for test prupose. It add a button (that manage an alert) and a select (that allow to insert tags) in the toolbar.
 * This plugin also disable the "f" key in the editarea, and load a CSS and a JS file
 */  
var EditArea_testcode = {
	onkeydown: function(e){
		if (e.shiftKey && e.keyCode == 13) {
			window.top.test_code();
			return false;
		}
	}};

// Adds the plugin class to the list of available EditArea plugins
editArea.add_plugin("testcode", EditArea_testcode);
