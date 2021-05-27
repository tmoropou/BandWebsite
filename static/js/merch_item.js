// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        rows: [],
        stars: 5,
        write_review: false,
        review_body: "",
        logged_in: false,
        item: {}
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.toggle_review = function () {
        app.vue.write_review = !app.vue.write_review;
        app.vue.review_body = "";
    }

    app.set_star = function (count) {
        app.vue.stars = count;
    }

    app.submit_review = function () {
        console.log(app.vue.stars, app.vue.review_body);
        app.toggle_review();
    }

    app.check_logged = () => {
        if(global_email != "None"){
            app.vue.logged_in = true;
            return true;
        }
        return false;
    }

    app.methods = {
        toggle_review: app.toggle_review,
        set_star: app.set_star,
        submit_review: app.submit_review,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
        // Do any initializations (e.g. networks calls) here.
        app.vue.item = item;
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
