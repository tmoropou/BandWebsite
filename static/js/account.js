// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        first_name: "",
        last_name: "",
        user_name: "",
        user_email: "",
        user_password: "",
        rows: [],
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.create_user = function () {
        axios.post(create_user_url,
            {
                first_name: app.vue.first_name,
                last_name: app.vue.last_name,
                user_name: app.vue.user_name,
                user_email: app.vue.user_email,
                user_password: app.vue.user_password,
            }).then(function (response) {
            app.vue.rows.push({
                id: response.data.id,
                first_name: app.vue.first_name,
                last_name: app.vue.last_name,
                user_name: app.vue.user_name,
                user_email: app.vue.user_email,
                user_password: app.vue.user_password,
            });
            app.enumerate(app.vue.rows);
        });
    };

    app.methods = {
        create_user: app.create_user,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
        // Do any initializations (e.g. networks calls) here.
//        axios.get(check_admin_url).then(function (response) {
//            if (response.data.admin > 0){
//                app.vue.admin_flag = true;
//            }
//        });
        // app.create_user();
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
