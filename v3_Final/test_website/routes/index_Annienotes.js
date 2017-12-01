Frontend_Controller - interprets button inputs from Python Controller,
and manage the view, keeping track of current state and updating from JS Model
(not sure of a better way to describe this purpose pls change)

map_pos = (zoom_level, center_coordinate)

button_input_handler([any_input]) reads from json file

[map_pos, map_bounds] = zoom_pan_handler([zoom/pan]_button_input, map_pos)

map_pos contains ID of map image, which corresponds to center position and zoom level

map_bounds contains abs (GPS) bounds of current map view

[Mapping stuff with help from John]

add_waypoint_annotation(waypoint_id?, annotation) used for sending annotations to Hive queue on backend controller

/**
 * The Controller. Controller responds to user actions and
 * invokes changes on the model.
 */
 /////////////////////////////////////////////////
var Routes = function (model, view) {
    this.view = view;
    this.model = model;

    this.init();
};

Routes.prototype = {

    init: function () {
        this.setupHandlers()
            .enable();
    },

    setupHandlers: function () {

        this.addTaskHandler = this.addTask.bind(this);
        this.selectTaskHandler = this.selectTask.bind(this);
        this.unselectTaskHandler = this.unselectTask.bind(this);
        this.completeTaskHandler = this.completeTask.bind(this);
        this.deleteTaskHandler = this.deleteTask.bind(this);
        return this;
    },

    enable: function () {

        this.view.addTaskEvent.attach(this.addTaskHandler);
        this.view.completeTaskEvent.attach(this.completeTaskHandler);
        this.view.deleteTaskEvent.attach(this.deleteTaskHandler);
        this.view.selectTaskEvent.attach(this.selectTaskHandler);
        this.view.unselectTaskEvent.attach(this.unselectTaskHandler);

        return this;
    },


    addTask: function (sender, args) {
        this.model.addTask(args.task);
    },

    selectTask: function (sender, args) {
        this.model.setSelectedTask(args.taskIndex);
    },

    unselectTask: function (sender, args) {
        this.model.unselectTask(args.taskIndex);
    },

    completeTask: function () {
        this.model.setTasksAsCompleted();
    },

    deleteTask: function () {
        this.model.deleteTasks();
    }

};
