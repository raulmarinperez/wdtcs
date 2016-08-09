var libwdtcs = libwdtcs || function () {};

// fn: set_webix
// args: - webix - Reference to the instantiated webix framework.
// desc: Set an internal reference to the webix framework.
libwdtcs.prototype.set_webix = function(webix) {
  this._webix = webix;
}

// fn: set_application_width
// args: - width - Store current GUI width.
// desc: Set the width of the applicatin to be consider for positioning.
libwdtcs.prototype.set_application_width = function(width) {
  this._width = width;
}

// fn: start
// args: -
// desc: Initiate the GUI and display the main screen
libwdtcs.prototype.start = function() {
    var dummy_contents = { id:"contents",
                           template:"Contents to replace." };
    var k_pc = { cols:[ this.build_sidebar(), dummy_contents ] };
    // display the layout and setup the application
    var layout = { id:"layout", view:"layout",
                   rows: [ this.build_toolbar(), k_pc ] };
    this._webix.ui(layout, $$('layout'));
    this.set_application_width($$('layout').$width);
}

// fn: build_toolbar
// desc: Buid the toolbar at the top of the window.
libwdtcs.prototype.build_toolbar = function() {

  var tb_logo = { id:"tb_logo", view:"label", label:"This is the logo." }
  var tb = { id:"tb", view:"toolbar", cols:[ tb_logo] };

  return tb;
}

// fn: build_sidebar
// desc: Build the sidebar with different menus and options.
libwdtcs.prototype.build_sidebar = function() {
  var sb_data = [ { id: "sb_main", view:"menu", icon: "dashboard",
                    value: "sb_main",
                    data:[ { id: "dashboard1", value: "Dashboard 1"},
                           { id: "dashboard2", value: "Dashboard 2"} ] },
                  { id: "sb_students", icon: "columns",
                    value: "sb_students",
                    data:[ { id: "sb_students.new",
                             value: "sb_students_new" },
                           { id: "sb_students.list",
                             value: "sb_students_list" } ] },
                  { id: "sb_instructors", icon: "columns",
                    value: "sb_instructors",
                    data:[ { id: "accordions1", value: "Accordions"},
                           { id: "portlets1", value: "Portlets"} ] },
                  { id: "sb_activities", icon: "table",
                    value: "sb_activities",
                    data:[ { id: "tables1", value: "Datatable"},
                           { id: "tables2", value: "TreeTable"},
                           { id: "tables3", value: "Pivot"} ] },
                  { id: "sb_reports", icon: "table",
                    value: "sb_reports",
                    data:[ { id: "tables11", value: "Datatable"},
                           { id: "tables22", value: "TreeTable"},
                           { id: "tables33", value: "Pivot"} ] } ];

  var sb = { id:"sb", view:"sidebar", height: "auto", data:sb_data,
             on: { onAfterSelect: (id) => { this._show_menu(id); } }
           };

  return sb;
}
