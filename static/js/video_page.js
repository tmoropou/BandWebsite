// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        rows: [],
        video_id: 0,
        add_comment_body: "",
        admin_flag: 0
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.reload_comments = function () {
        let load_comments_url_id = load_comments_url + "/" + app.vue.video_id;
        axios.get(load_comments_url_id).then(function (response) {
            app.vue.rows = app.enumerate(response.data.rows);
        });        
    }

    app.add_comment = function() {
        let vid_comment_url = add_comment_url + "/" + app.vue.video_id;
        console.log('testing', vid_comment_url)
        axios.post(vid_comment_url,
            {
                body: app.vue.add_comment_body,
            }
        ).then(function (response) {
            app.reload_comments();
            app.vue.add_comment_body = "";
        });
    }

    app.methods = {
        add_comment: app.add_comment,
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
            app.vue.admin_flag = response.data.admin;
        });
        app.vue.video_id=video_id;
        app.reload_comments();
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
