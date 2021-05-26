// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        rows: [],
        admin_flag: false,
        logged_in: false,
        editing: {
            'name': false,
            'cost': false,
            'description': false,
            'image_path': false,
            'type': false,
            'stock': false,
        },
        item: {}
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.check_logged = () => {
        if(global_email != "None"){
            app.vue.logged_in = true;
            return true;
        }
        return false;
    }

    app.toggle_edit = function (key) {
        if(key in app.vue.editing){
            app.vue.editing[key] = !app.vue.editing[key];
        }
        return;
    }

    app.edit_field = function (key) {
        if(key === "stock"){
            let as_int = parseInt(app.vue.item.stock);
            if(isNaN(as_int)){
                app.vue.item.stock = 0;
            } else {
                app.vue.item.stock = as_int;
            }
        }
        
        // I can't get this to handle floats properly
        // So I'm just going to handle that in the backend
        if(key === "cost"){
            let as_float = parseFloat(app.vue.item.cost);
            if(isNaN(as_float)){
                app.vue.item.cost = 0;
            } else {
                app.vue.item.cost = parseFloat(as_float);
            }
        }

        console.log(app.vue.item);
        axios.post(update_item_url,
            {
                body: app.vue.item,
            }).then(function (response) {
                if(Number.isInteger(response.data.id)) {
                    app.vue.item.id = response.data.id;
                }
            }
        );
        app.toggle_edit(key);
    }

    app.methods = {
        toggle_edit: app.toggle_edit,
        edit_field: app.edit_field,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
        // Do any initializations (e.g. networks calls) here.
        axios.get(check_admin_url).then(function (response) {
            if (response.data.admin > 0){
                app.vue.admin_flag = true;
            }
        });
        app.check_logged();
        app.vue.item = item;
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
